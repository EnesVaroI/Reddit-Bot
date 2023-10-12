import json

def save_json(file_path, data, mode='w'):
    with open(file_path, mode) as file:
        json.dump(data, file, indent=4)

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
      
    except FileNotFoundError:
        return None

def format_json(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    
    formatted_json = data.replace("\n][", ",")
    
    with open(file_path, 'w') as file:
        file.write(formatted_json)