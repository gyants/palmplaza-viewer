from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from flask_ngrok import run_with_ngrok
from flask import Flask, request, abort
import requests
import json
from utils.web_scraper import get_topics, read_replies
from utils.data_utils import sort_by, extract_field, extract_topics_id
from utils.line_objects_utils import reply_carousel, forum_carousel

from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)
run_with_ngrok(app)
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
parser = WebhookParser(CHANNEL_SECRET)


@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    for event in events:
        if event.type == 'message':

            if event.message.text.startswith('read'):
                identifier = event.message.text.split('read')[1].strip()
                replies = read_replies(identifier)
                replies = sort_by(replies, 'number')
                carousel = reply_carousel(replies)
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(alt_text='Replies',
                                    contents=carousel)
                )
            else:
                all_topics = get_topics()
                carousel = forum_carousel(all_topics)
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(alt_text='Forum',
                                    contents=carousel)
                )

        if event.type == 'postback':
            data = event.postback.data.split('&')
            action, identifier = data[0].split('=')[1], data[1].split('=')[1]
            replies = read_replies(identifier)
            replies = sort_by(replies, 'number')
            carousel = reply_carousel(replies)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='Replies',
                                contents=carousel)
            )

    return 'OK'


if __name__ == "__main__":
    app.run()
