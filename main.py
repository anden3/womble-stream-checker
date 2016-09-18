import os
import re
import praw
import requests
import threading

reddit = None
subreddit = None
last_status = None
clientCallback = 'http://127.0.0.1:65010/authorize_callback'

twitchHeaders = {
    'Client-ID': os.environ['TWITCH_ID']
}

rightPaddingRegex = re.compile(r"(twitch\.tv\/SovietWomble\"\] \{(\n.+)+)padding-right: (\d)px;")

liveCss = '\n\n\
.side .md [href="https://www.twitch.tv/SovietWomble"]::after {\n\
    content: "LIVE!";\n\
    border: 3px solid red;\n\
    background-color: red;\n\
    margin-left: 10px;\n\
    animation: live 1s linear infinite;\n\
}'


def init_reddit():
    clientID = os.environ['REDDIT_ID']
    clientSecret = os.environ['REDDIT_SECRET']
    refresh_token = os.environ['REFRESH_TOKEN']
    
    global reddit, subreddit
    reddit = praw.Reddit('Womble Stream Checker v0.1 by /u/anden3')
    subreddit = reddit.get_subreddit('sovietwomble')
    
    reddit.config.decode_html_entities = True

    reddit.set_oauth_app_info(client_id=clientID, client_secret=clientSecret, redirect_uri=clientCallback)
    reddit.refresh_access_information(refresh_token)


def get_twitch_status():
    request = requests.get("https://api.twitch.tv/kraken/streams/sovietwomble", headers=twitchHeaders).json()
    return request["stream"] != None


def change_stylesheet(live):
    global reddit, subreddit
    stylesheet = subreddit.get_stylesheet()['stylesheet']
    afterCssExists = stylesheet.find("animation: live") != -1
    
    mr = rightPaddingRegex.search(stylesheet)
    stylesheetList = list(stylesheet)
    
    if live:
        stylesheetList[mr.start(3):mr.end(3)] = "0";
        stylesheet = ''.join(stylesheetList)
        
        if not afterCssExists:
            stylesheet += liveCss
    
    else:
        stylesheetList[mr.start(3):mr.end(3)] = "4";
        stylesheet = ''.join(stylesheetList)
                
        if afterCssExists:
            stylesheet = stylesheet[:-len(liveCss)]
    
    subreddit.set_stylesheet(stylesheet)

def loop():
    global last_status
    
    threading.Timer(10.0, loop).start()
    twitch_status = get_twitch_status()
    
    if twitch_status != last_status:
        last_status = twitch_status
        change_stylesheet(last_status)

init_reddit()
loop()