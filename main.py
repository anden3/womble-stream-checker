import os
import praw
import requests
import threading

reddit = None
last_status = False
clientCallback = 'http://127.0.0.1:65010/authorize_callback'


def init_reddit():
    try:
        clientID = os.environ['REDDIT_ID']
        clientSecret = os.environ['REDDIT_SECRET']
        refresh_token = os.environ['REFRESH_TOKEN']

    except KeyError:
        clientID = 'SR84ToXmUjfzfQ'
        clientSecret = 'SMmzNu3m_QBubneR4-gQb0tX-F8'
        refresh_token = "62832500-cAD5izvDolVo3krTD6fPhQwu0T0"
    
    global reddit
    reddit = praw.Reddit('Womble Stream Checker v0.1 by /u/anden3')

    reddit.set_oauth_app_info(client_id=clientID, client_secret=clientSecret, redirect_uri=clientCallback)
    reddit.refresh_access_information(refresh_token)


def get_twitch_status():
    return requests.get("https://api.twitch.tv/kraken/streams/sovietwomble").json()["stream"] != "null"


def loop():
    global reddit, last_status
    
    threading.Timer(300.0, loop).start()
    twitch_status = get_twitch_status()
    
    if twitch_status != last_status:
        last_status = twitch_status
        
        stylesheet = reddit.get_stylesheet("sovietwomble")
        print(stylesheet)

init_reddit()
loop()