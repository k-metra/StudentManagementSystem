import json

import json

def load_accounts(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)

    return data.get('accounts', [])

def access_file(file_name):
    accounts = load_accounts(file_name)
    print(accounts) 
    if accounts:
        first = accounts[0]
        print(f"name: {first['username']}, password: {first['password']}")

def prompt_login():
    print("Enter your username: ", end="", flush=True)
    username = input()
    print("Enter your password: ", end="", flush=True)
    password = input()
    return username, password


