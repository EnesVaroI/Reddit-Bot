import praw
import time
from post_archiving import archive_document
from json_handler import save_json, load_json, format_json
from post_management import ManagePosts

def run_bot(reddit):
    subreddit = reddit.subreddit("plantclinic")
    post_tracker = load_json('post_data.json')

    manage = ManagePosts(reddit, post_tracker)
  
    while True:
        for submission in subreddit.new(limit=10):
            try:
                manage.send_messages(submission)

            except praw.exceptions.RedditAPIException as e:
                manage.process_blacklisted_posts(e, submission)
              
        save_json('post_data.json', post_tracker)
        
        for message in reddit.inbox.all(limit=10):
            post_id = manage.find_post(message)
          
            if post_id is not None:
                manage.process_active_posts(post_id, message)

        save_json('post_data.json', post_tracker)
    
        archived_logs = []
      
        for post_id, post_data in post_tracker.items():
            manage.process_inactive_posts(post_id, post_data)

            archive_document(post_id, post_data, archived_logs)

        save_json('post_data.json', post_tracker)
      
        if archived_logs:
            save_json('archived_logs.json', archived_logs, 'a')
            format_json('archived_logs.json')
      
        for archived_document in archived_logs:
            del post_tracker[archived_document["post_id"]]
    
        save_json('post_data.json', post_tracker)
              
        time.sleep(60)
