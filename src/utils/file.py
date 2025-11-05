import json

def load_file(file_name, is_json=True, key=None):

    # Wrap JSON parsing in try-except to handle malformed JSON or missing files 
    try:
        with open(file_name) as file:

            try:
                data = json.load(file) if is_json else file.read()
            except json.JSONDecodeError:
                data = {}
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Returning empty data.")
        data = {} if is_json else ""

    return data.get(key) if key and is_json else data  