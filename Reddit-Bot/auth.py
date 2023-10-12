import praw
import os

def authenticate():
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="botscript by me",
        username=username,
        password=password
    )

    return reddit