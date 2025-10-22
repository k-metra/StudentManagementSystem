import sys
import time
from .file import load_file
from .misc import clear_input_buffer

def prompt_login():
    # Small delay and clear input buffer to prevent keyboard event interference
    time.sleep(0.1)
    clear_input_buffer()
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username, password


