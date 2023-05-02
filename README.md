# PalmPlaza Viewer 

**What? :** This is a LINE chatbot wrapper for [PalmPlaza's "EViL" forum](http://www.palm-plaza.com/cgi-bin/CCforum/board.cgi?az=list&forum=DCForumID4&archive=)

**How? :** This works by scraping PalmPlaza's "EViL" forum and present it in a more beautiful way- via LINE! in the form of chatbot

**For whom? :** For the gays who love cruising!

## Features 
<img src=/assets/IMG_1305.jpeg width="306" height="600"> <img src=/assets/IMG_1306.png width="432" height="600">
- View the forum via Rich Menu
- View up to **10** latest replies by tapping the topic
- Reply to a message on the web via buttons

## Limitations
- Host computer needs to be online to use the bot
- Long response time to taps/messages

## Requirements
- [Python](https://www.python.org/)
- [ngrok](https://ngrok.com/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [flask-ngrok](https://pypi.org/project/flask-ngrok/)
- LINE Official Account (LINE OA)

## How to get started
1. Create a .env file in the root folder
2. Set `CHANNEL_ACCESS_TOKEN` to your LINE OA's channel access token
3. Set `CHANNEL_SECRET` to your LINE OA's channel secret
4. Run `main.py`
