import json
from config_model import SubredditConfig

def read_config_file(file_path):
    with open(file_path, 'r') as config_file:
        config_data = json.load(config_file)
        subreddit_data = [SubredditConfig.from_json(data) for data in config_data]
    return subreddit_data

def write_config_file(file_path, subreddit_data):
    json_data = [config.to_json() for config in subreddit_data]
    with open(file_path, 'w') as config_file:
        json.dump(json_data, config_file, indent=4)