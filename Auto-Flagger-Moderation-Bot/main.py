import os

from sklearn.pipeline import make_union
from config_handler import read_config_file
from bot import RedditModerationBot

bot = RedditModerationBot(
    os.environ['YOUR_CLIENT_ID'],
    os.environ['YOUR_CLIENT_SECRET'],
    os.environ['YOUR_USER_AGENT'],
    os.environ['YOUR_REDDIT_USERNAME'],
    os.environ['YOUR_REDDIT_PASSWORD']
)

config = read_config_file('config.json')

for subreddit_data in config:
    bot.run_bot(subreddit_data, limit=10)