import time
from comment_assessment import CommentAssessment
from reddit_API_interaction import RedditAPI
from notificationLogger import NotificationLogger
from DB_module import DatabaseManager

class RedditModerationBot:
    def __init__(self, client_id, client_secret, user_agent, username, password, log_file='bot.log', database_name='reddit_bot.db'):
        self.reddit_api = RedditAPI(client_id, client_secret, user_agent, username, password)
        self.notification_logger = NotificationLogger(log_file, self.reddit_api.reddit)
        self.database_manager = DatabaseManager(database_name)
        
        self.comment_assessment = CommentAssessment()
    
    def __assess_and_moderate_comments(self, subreddit, limit=10):
        try:
            comments = self.reddit_api.get_comments(subreddit.name, limit)
            
            for comment in comments:
                relevance_score = self.comment_assessment.assess_comment_relevance(comment.text, subreddit.keywords)
                
                toxicity_score = self.comment_assessment.assess_comment_toxicity(comment.text)
                
                is_spam = self.comment_assessment.assess_comment_spam(comment.text)
                
                breaks_rules = self.comment_assessment.assess_comment(comment.text, subreddit.rules)
                
                total_score = relevance_score + toxicity_score + is_spam + breaks_rules
                
                comment_data = {
                    'comment_id': comment.id,
                    'username': comment.author.name,
                    'comment_text': comment.text,
                    'relevance_score': relevance_score,
                    'toxicity_score': toxicity_score,
                    'spam_score': is_spam,
                    'breaks_rules_score': breaks_rules,
                    'total_score': total_score
                }
                self.database_manager.create_comment(comment_data)
                
                self.database_manager.update_user_score(comment.author.name, total_score)
                
                user_total_score = self.database_manager.get_user_score(comment.author.name)
                if user_total_score >= 25 and user_total_score < 50: # Feel free to replace the hardcoded numbers to your liking here
                    subreddit.banned.add(comment.author.name, duration=30, ban_reason='Violating subreddit rules')
                    self.notification_logger.send_notification(
                        f'{comment.author.name} has been issued a 30-day ban.',
                        subreddit
                    )
                elif user_total_score >= 50:
                    subreddit.banned.add(comment.author.name, note='Repeated violations of subreddit rules')
                    self.notification_logger.send_notification(
                        f'{comment.author.name} has been permanently banned.',
                        subreddit
                    )
        
        except Exception as e:
            self.notification_logger.log_error(f"An error occurred: {str(e)}")

    def run_bot(self, subreddit_data, limit=10):
        while True:
            self.__assess_and_moderate_comments(subreddit_data, limit)
            time.sleep(3600)