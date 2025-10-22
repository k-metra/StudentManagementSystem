import json

def load_file(file_name, is_json=True, key=None):
    with open(file_name) as file:
        data = json.load(file) if is_json else file.read()

    return data.get(key) if key and is_json else data  