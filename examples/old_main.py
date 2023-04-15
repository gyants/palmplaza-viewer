import forum
import jsontest
from flask import Flask, request, abort
from flask_ngrok import run_with_ngrok

from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)

app = Flask(__name__)
n = 1
run_with_ngrok(app)


line_bot_api = LineBotApi(
    '0Rf4tfkS9SAYSl3eHNJGY/7qa//LKpOBzXdkuPkHxdYGAz0uCHkD8lYbGAdTd7JkH2/9dbeVoW9D1P9MorfZCTYoZntWD+V43JbyeruSVAcBQUquCEglZbRhdUKmK7SGCJZ6LP2DmuV1cOlRozVzCQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('85c3a49fd8506e646bb679e889b1933a')
parser = WebhookParser('85c3a49fd8506e646bb679e889b1933a')


@app.route("/webhook", methods=['POST'])
def callback():
    global n
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        if event.message.text.lower() == 'forum':
            n = 1
            foruminfo = page(n)
            flex = jsontest.ForumBubble(foruminfo)
            flex.bubble['body']['contents'][0]['text'] = 'Page %d' % n
            if n == 1:
                flex.bubble['footer']['contents'].pop(0)
            flex = flex.getJson()
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='Forum',
                                contents=flex)
            )
        elif event.message.text.startswith('next'):
            if n < 4:
                n += 1
            else:
                n = 4
            foruminfo = page(n)
            flex = jsontest.ForumBubble(foruminfo)
            flex.bubble['body']['contents'][0]['text'] = 'Page %d' % n
            if n == 4:
                flex.bubble['footer']['contents'].pop()
            flex = flex.getJson()
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='Forum',
                                contents=flex)
            )
        elif event.message.text.lower() == 'previous':
            if n > 1:
                n -= 1
            else:
                n = 1
            foruminfo = page(n)
            flex = jsontest.ForumBubble(foruminfo)
            flex.bubble['body']['contents'][0]['text'] = 'Page %d' % n
            if n == 1:
                flex.bubble['footer']['contents'].pop(0)
            flex = flex.getJson()
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='Forum',
                                contents=flex)
            )
        elif event.message.text.startswith('forum ') or event.message.text.startswith('Forum '):
            title = event.message.text.split(' ')
            title = ' '.join(title[1:])
            foruminfo = callForum()
            foruminfo = foruminfo.search(title)
            if foruminfo:
                flex = jsontest.ForumBubble(foruminfo)
                flex.bubble['body']['contents'][0]['text'] = 'Including %s' % title
                flex.bubble.pop('footer', None)
                flex = flex.getJson()
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(alt_text='Forum',
                                    contents=flex)
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='No entries for keyword %s' % title)
                )

        elif event.message.text.startswith('view '):
            title = event.message.text.split('view ')[1]
            foruminfo = callForum()
            foruminfo = foruminfo.search(title)
            if type(foruminfo) == list:
                for i in foruminfo:
                    if title == i.topic:
                        foruminfo = i
                        break
            thread = foruminfo.fetchReplies()
            flex = jsontest.Carousel(repliesToCarousel(thread)).getJson()
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text=title,
                                contents=flex)
            )
        elif event.message.text.lower() == 'hottest':
            foruminfo = callForum().hottest()
            title = foruminfo.topic
            thread = foruminfo.fetchReplies()
            flex = jsontest.Carousel(repliesToCarousel(thread)).getJson()
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text=title,
                                contents=flex)
            )

        elif event.message.text.lower() == 'trending':
            foruminfo = callForum().trending()
            if foruminfo:
                flex = jsontest.ForumBubble(foruminfo)
                flex.bubble.pop('footer', None)
                flex = flex.getJson()
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(alt_text='Trending',
                                    contents=flex)
                )
        elif event.message.text.startswith('past ') or event.message.text.startswith('Past '):
            time = event.message.text.split(' ')
            time = ' '.join(time[1:])
            time = int(time)
            foruminfo = callForum().pastMinutes(time)
            if foruminfo:
                flex = jsontest.ForumBubble(foruminfo)
                flex.bubble['body']['contents'][0]['text'] = 'Past %d minutes' % time
                flex.bubble.pop('footer', None)
                flex = flex.getJson()
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(alt_text='Past %d minutes' % time,
                                    contents=flex)
                )

    return 'OK'


def repliesToCarousel(repliesList):
    toCarousel = []
    for i in repliesList:
        temp = i.getReply()
        bubble = jsontest.ReplyBubble(temp)
        toCarousel.append(bubble)
    return toCarousel


def callForum():
    foruminfo = forum.Forum()
    foruminfo.prettify()
    return foruminfo


def page(n):
    topics = callForum().threads
    if n <= 1:
        return topics[:30]
    elif n == 2:
        return topics[30:60]
    elif n == 3:
        return topics[60:90]
    else:
        return topics[90:]


if __name__ == "__main__":
    app.run()
