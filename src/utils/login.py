import json

def access_file(file_name):
    with open(file_name, 'r') as file:
        account =  json.load(file)
    # just to test and visualize if the code works
    return json.dumps(account, indent=4)

