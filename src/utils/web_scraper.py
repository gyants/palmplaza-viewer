import requests
from datetime import datetime
from bs4 import BeautifulSoup

URL = 'https://www.palm-plaza.com/cgi-bin/CCforum/board.cgi?az=list&forum=DCForumID4&archive='


def fetch_div():
    '''
    Fetch the starting div where all topics are in 
    '''
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser',
                         from_encoding='tis-620')
    return soup.find('div', align='left')


class TopicExtractor:
    '''
    Topic extractor class, not recommended since get_topics() already wrapped this for you
    '''

    def __init__(self, div_element):
        self.data = []
        self.temp_info = []
        self.temp = {'topic': '',
                     'url': '',
                     'author': '',
                     'lastreplied': '',
                     'replies': ''}
        self.div = div_element

    def extract_tags_from_div(self, div):
        """
        Extracts the desired tags (e.g. <a>, <font>) from a given div and its nested divs recursively.
        """
        for child in div.children:
            if child.name == 'div':
                self.temp['author'] = self.temp_info[0]
                self.temp_info[1] = self.temp_info[1].strip('[').strip(']')
                self.temp['lastreplied'] = datetime.strptime(
                    self.temp_info[1], '%d-%b-%y , %H:%M %p')
                self.temp['replies'] = int(
                    self.temp_info[2].strip('(').strip(')'))
                self.data.append(self.temp)
                self.temp_info = []
                self.temp = {'topic': '',
                             'url': '',
                             'author': '',
                             'lastreplied': '',
                             'replies': ''}
                self.extract_tags_from_div(child)
            elif child.name == 'a':
                if not child.find('img'):
                    # print(child['href'])
                    self.temp['url'] = child['href'].strip()
                    # print(child.text)
                    self.temp['topic'] = child.text.strip()
            elif child.name == 'font':
                # print(child.text)
                self.temp_info.append(child.text.replace(
                    '\xa0', ' ').replace('\n', ''))

    def get_data(self):
        self.extract_tags_from_div(self.div)
        return self.data[1:]


def get_topics():
    '''
    Get all topics in the forum
    '''
    extractor = TopicExtractor(fetch_div())
    return extractor.get_data()


def fetch_replies_table(topic_url):
    '''
    Fetch the replies in a topic of the given url
    '''
    response = requests.get(topic_url)
    soup = BeautifulSoup(response.content, 'html.parser',
                         from_encoding='tis-620')
    replies = soup.find_all(
        'table', border=0, width='100%', cellpadding=3, cellspacing=0)
    return replies


def parse_reply_data(reply):
    '''
    Parse the data in the reply table. Used in for loop 
    '''
    replyinfo = reply.find('td', valign='top').text.split('\n')
    time = reply.find_all('font', size='1', face='Tahoma', color="#3F007F")
    body = reply.find('td', valign='top', width='100%')
    return replyinfo, time, body


def read_replies(topic_url):
    '''
    Read all replies in a topic
    '''
    replies = fetch_replies_table(topic_url)
    parsed_replies = []
    for reply in replies:
        temp = {'author': '', 'number': '', 'time': '', 'message': ''}
        try:
            replyinfo, time, body = parse_reply_data(reply)
            for br in body.find_all("br"):
                br.replace_with("\n")
            temp['author'] = replyinfo[2]
            num = replyinfo[7].split(' ')[0][:-1]
            temp['number'] = 0 if num == '' else int(num)
            for i in time:
                if 'Asia' in i.text:
                    temp['time'] = datetime.strptime(
                        i.text.strip(), "%d-%b-%y, %I:%M %p (%Z)")
            temp['message'] = body.text.strip()
            parsed_replies.append(temp)
        except:
            pass
    return parsed_replies
