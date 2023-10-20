import time
from canned_messages import (
    bot_message,
    additional_information_message,
    inactive_post_removal_message,
    blacklisted_post_removal_message
)

class ManagePosts:
    def __init__(self, reddit, post_tracker):
        self.reddit = reddit
        self.post_tracker = post_tracker

    def send_messages(self, submission):
        post_id = submission.id
        post_approved = submission.approved
        word_count = len(submission.selftext.split())
        post_age = int(time.time() - submission.created_utc)
        post_age_threshold = 3 * 3600
    
        if post_id not in self.post_tracker and post_age <= post_age_threshold and not post_approved and word_count < 40:
            op = submission.author
            if op:
                op_message = bot_message()
    
                op.message("Request for Context", op_message)
    
                message = next(self.reddit.inbox.sent(limit=1))
                self.post_tracker[post_id] = {
                    "message_id": message.id,
                    "op_responded": False,
                    "timestamp": time.time(),
                    "post_removed": False
                }
    
    def process_blacklisted_posts(self, e, submission):
        if "NOT_WHITELISTED_BY_USER_MESSAGE" in str(e):
            comment = submission.reply(blacklisted_post_removal_message())
            comment.mod.distinguish(how='yes', sticky=True)
            comment.mod.lock()
    
            submission.mod.remove()
            submission.mod.lock()
    
    def find_post(self, message):
        for post_id, value in self.post_tracker.items():
            if value.get("message_id") == str(message.parent_id)[3:]:
                return post_id
        return None
    
    def process_active_posts(self, post_id, message):
        submission = self.reddit.submission(id=post_id)
      
        if submission and not self.post_tracker[post_id]["op_responded"]:
            comment = submission.reply(additional_information_message(message.body))
            comment.mod.distinguish(how='yes', sticky=True)
            comment.mod.lock()
    
            if self.post_tracker[post_id]["post_removed"]:
                submission.mod.approve()
                submission.mod.unlock()
    
                for comment in submission.comments:
                    if comment.author.name == self.reddit.user.me().name and "Your post has been removed" in comment.body:
                        comment.delete()
    
                self.post_tracker[post_id]["post_removed"] = False
          
            self.post_tracker[post_id]["op_responded"] = True
    
    def process_inactive_posts(self, post_id, post_data):
        inactivity_threshold = 600
        elapsed_time = int(time.time() - post_data["timestamp"])
    
        if not post_data["post_removed"] and elapsed_time >= inactivity_threshold and not post_data["op_responded"]:
            submission = self.reddit.submission(id=post_id)
    
            if submission.approved or len(submission.selftext.split()) >= 40:
                return
    
            submission.mod.remove()
            submission.mod.lock()
          
            comment = submission.reply(inactive_post_removal_message())
            comment.mod.distinguish(how='yes', sticky=True)
            comment.mod.lock()
    
            post_data["post_removed"] = True
