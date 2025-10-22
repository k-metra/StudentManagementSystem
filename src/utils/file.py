import json

def load_file(file_name, isJson=True, key=None):
    with open(file_name) as file:
        data = json.load(file) if isJson else file.read()

    return data.get(key) if key and isJson else data  