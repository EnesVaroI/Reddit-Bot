import praw
from psaw import PushshiftAPI

class RedditAPI:
    def __init__(self, client_id, client_secret, user_agent, username, password):
        self.reddit = praw.Reddit(
            client_id = client_id,
            client_secret = client_secret,
            user_agent = user_agent,
            username = username,
            password = password
        )

    def get_comments(self, subreddit, limit=10):
        try:
            subreddit_obj = self.reddit.subreddit(subreddit)
            comments = []
            for submission in subreddit_obj.hot(limit=limit):
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                    comments.append(comment.body)
            return comments
        except Exception as e:
            print(f"Error retrieving comments: {str(e)}")
            return []

    def post_comment(self, submission_id, comment_text):
        try:
            submission = self.reddit.submission(id=submission_id)
            submission.reply(comment_text)
            return True
        except Exception as e:
            print(f"Error posting comment: {str(e)}")
            return False

    def send_private_message(self, recipient, subject, message):
        try:
            self.reddit.redditor(recipient).message(subject, message)
            return True
        except Exception as e:
            print(f"Error sending private message: {str(e)}")
            return False