import praw
import time
from post_archiving import archive_document
from json_handler import save_json, load_json, format_json
from post_management import (
    send_messages,
    process_blacklisted_posts,
    find_post,
    process_active_posts,
    process_inactive_posts
)

def run_bot(reddit):
    subreddit = reddit.subreddit("plantclinic")
    post_tracker = load_json('post_data.json')

    while True:
        for submission in subreddit.new(limit=10):
            try:
                send_messages(submission, reddit, post_tracker)

            except praw.exceptions.RedditAPIException as e:
                process_blacklisted_posts(e, submission)
              
        save_json('post_data.json', post_tracker)
        
        for message in reddit.inbox.all(limit=10):
            post_id = find_post(message, post_tracker)
          
            if post_id is not None:
                process_active_posts(post_id, reddit, message, post_tracker)

        save_json('post_data.json', post_tracker)
    
        archived_logs = []
      
        for post_id, post_data in post_tracker.items():
            process_inactive_posts(reddit, post_id, post_data)

            archive_document(post_id, post_data, archived_logs)

        save_json('post_data.json', post_tracker)
      
        if archived_logs:
            save_json('archived_logs.json', archived_logs, 'a')
            format_json('archived_logs.json')
      
        for archived_document in archived_logs:
            del post_tracker[archived_document["post_id"]]
    
        save_json('post_data.json', post_tracker)
              
        time.sleep(60)