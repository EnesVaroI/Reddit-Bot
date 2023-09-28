import logging
import praw

class NotificationLogger:
    def __init__(self, log_file, reddit):
        self.log_file = log_file
        self.reddit = reddit
        self.initialize_logger()

    def initialize_logger(self):
        self.logger = logging.getLogger('reddit_bot')
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def send_notification(self, message, subreddit_name):
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            subreddit.message('Notification from Bot', message)
            self.logger.info(f"Sent modmail notification to /r/{subreddit_name} moderators: {message}")
        except Exception as e:
            self.logger.error(f"Failed to send modmail notification: {str(e)}")