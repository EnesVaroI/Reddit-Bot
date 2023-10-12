import time

def archive_document(post_id, post_data, archived_logs):
    data_archive_threshold = 6 * 3600
    elapsed_time = int(time.time() - post_data["timestamp"])
  
    if elapsed_time >= data_archive_threshold:
        archived_document = {"post_id": post_id, **post_data}
        archived_logs.append(archived_document)
  