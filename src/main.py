import requests
import json
from utils.web_scraper import get_topics, read_replies
from utils.data_utils import sort_by, extract_field, extract_topics_id
from utils.line_objects_utils import reply_carousel

all_topics = get_topics()
hottest = sort_by(all_topics, 'replies')[0]
replies = read_replies(hottest)
reply = replies[-5]
print(reply)