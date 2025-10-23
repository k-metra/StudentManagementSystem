import sys
import time
from .file import load_file
from .misc import clear_input_buffer
import pwinput

def prompt_login():
    # Small delay and clear input buffer to prevent keyboard event interference
    time.sleep(0.1)
    clear_input_buffer()
    
    username = input("Enter username: ")

    # Instead of the traditional input(), we use pwinput to mask password input with
    # asterisks, enhancing security and mirroring typical login behavior.
    password = pwinput.pwinput("Enter password: ")
    return username, password


