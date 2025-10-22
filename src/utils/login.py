from .file import load_file

def load_accounts(file_name):
    return load_file(file_name, key="accounts")

def prompt_login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username, password


