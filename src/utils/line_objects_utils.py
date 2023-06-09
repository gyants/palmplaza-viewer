import json
import sys
import os
from datetime import datetime, timedelta

file_path = sys.path[0]


def time_ago(dt):
    delta = datetime.now() - dt
    if delta < timedelta(minutes=1):
        return "เมื่อกี้"
    elif delta < timedelta(hours=1):
        minutes = delta.seconds // 60
        if minutes == 1:
            return "1 นาทีที่แล้ว"
        else:
            return f"{minutes} นาทีที่แล้ว"
    elif delta < timedelta(days=1):
        hours = delta.seconds // 3600
        if hours == 1:
            return "1 ชั่วโมงก่อน"
        else:
            return f"{hours} ชั่วโมงที่แล้ว"
    else:
        days = delta.days
        if days == 1:
            return "1 วันที่แล้ว"
        else:
            return f"{days} วันที่แล้ว"


def load_topic_replies():
    path = os.path.join(file_path, "utils", "templates", "topic_replies.json")
    with open(path, encoding="utf8") as fp:
        return json.load(fp)


def load_forum_bubble_page():
    path = os.path.join(file_path, "utils", "templates", "forum_bubble_page.json")
    with open(path, encoding="utf8") as fp:
        return json.load(fp)


def load_quoted_message():
    path = os.path.join(file_path, "utils", "templates", "quoted_message.json")
    with open(path, encoding="utf8") as fp:
        return json.load(fp)


def load_reply_bubble():
    path = os.path.join(file_path, "utils", "templates", "reply_bubble.json")
    with open(path, encoding="utf8") as fp:
        return json.load(fp)


def load_party_menu_carousel():
    path = os.path.join(file_path, "utils", "templates", "party_menu_carousel.json")
    with open(path, encoding="utf8") as fp:
        return json.load(fp)


def topic_replies_box(topic_dict):
    template = load_topic_replies()
    name = topic_dict["topic"]
    replies = topic_dict["replies"]
    topic_id = (
        topic_dict["url"]
        .split("https://www.palm-plaza.com/CCforum/DCForumID4/")[1]
        .split(".")[0]
    )
    topic_name_dict = dict(
        type="text",
        text=name,
        #    wrap=True,
        color="#D49BF6",
        flex=6,
        gravity="center",
        action=dict(type="postback", data="action=read&id=%s" % topic_id),
    )
    replies_dict = dict(
        type="text",
        text=str(replies),
        flex=2,
        color="#F5F5F5",
        align="center",
        gravity="center",
    )
    template["contents"].append(topic_name_dict)
    template["contents"].append(replies_dict)
    return template


def separate_10_topics(dict_list):
    templist = []
    separated = []
    for item in range((len(dict_list) // 10) + 1):
        for j in range(10):
            try:
                index = (item * 10) + j
                current_item = dict_list[index]
                templist.append(topic_replies_box(current_item))
            except:
                pass
        separated.append(templist)
        templist = []
    return separated


def forum_carousel(dict_list):
    carousel = dict(type="carousel", contents=[])
    pages = separate_10_topics(dict_list)
    current_page = 1
    for page in pages:
        bubble = load_forum_bubble_page()
        for topic in page:
            bubble["body"]["contents"].append(topic)
        bubble["header"]["contents"][1]["contents"][1]["text"] = "หน้า %d" % (
            current_page
        )
        current_page += 1
        carousel["contents"].append(bubble)

    return carousel


def message_to_lines(message):
    messages = message.split("\n")
    message_content = []
    for text in messages:
        if ">" in text:
            quote_template = load_quoted_message()
            cleaned_text = text.lstrip(">").strip()
            if cleaned_text not in ["", " "]:
                quote_template["contents"][1]["text"] = cleaned_text
                message_content.append(quote_template)
        else:
            normal_message = dict(
                type="text", text=text.strip(), color="#F5F5F5", wrap=True
            )
            message_content.append(normal_message)

    return message_content


def reply_bubble(reply_dict):
    template = load_reply_bubble()
    template["header"]["contents"][0]["text"] = reply_dict["topic"]
    template["header"]["action"]["uri"] = (
        "https://www.palm-plaza.com/CCforum/DCForumID4/%s.html" % reply_dict["topic_id"]
    )
    template["body"]["contents"][0]["text"] = reply_dict["author"]
    template["body"]["contents"][1]["contents"][0]["text"] += str(reply_dict["number"])
    template["body"]["contents"][1]["contents"][1]["text"] = time_ago(
        reply_dict["time"]
    )
    template["body"]["contents"][2]["contents"] = message_to_lines(
        reply_dict["message"]
    )
    template["footer"]["contents"][0]["action"]["uri"] += "%s&omm=%d" % (
        reply_dict["topic_id"],
        reply_dict["number"],
    )
    template["footer"]["contents"][1]["action"]["uri"] += "%s&omm=%d" % (
        reply_dict["topic_id"],
        reply_dict["number"],
    )
    return template


def reply_carousel(dict_list):
    carousel = dict(type="carousel", contents=[])
    available_items = dict_list[-10:]
    for reply_dict in available_items[::-1]:
        bubble = reply_bubble(reply_dict)
        carousel["contents"].append(bubble)

    return carousel


def party_carousel():
    carousel = load_party_menu_carousel()
    return carousel
