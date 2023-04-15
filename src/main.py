import requests
import json
from utils.web_scraper import get_topics, read_replies
from utils.data_utils import sort_by, extract_field, extract_topics_id
from utils.line_objects_utils import reply_carousel

all_topics = get_topics()
topic_1 = all_topics[1]
all_replies = read_replies(topic_1)

temp = reply_carousel(all_replies)
print(json.dumps(temp, indent=3))
