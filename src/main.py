import requests
from utils.web_scraper import get_topics, read_replies
from utils.data_utils import sort_by, extract_field, extract_topics_id, time_ago

all_topics = get_topics()
topic_1 = all_topics[0]
url_1 = topic_1['url']
all_replies = read_replies(url_1)
for i in all_replies:
    print(i['time'], time_ago(i['time']))
