import sys
import time
from .file import load_file

def load_accounts(file_name):
    return load_file(file_name, key="accounts")

def clear_input_buffer():
    """Clear any remaining input in the buffer to prevent interference from keyboard events"""
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        # For non-Windows systems
        import termios, tty
        sys.stdin.flush()

def prompt_login():
    # Small delay and clear input buffer to prevent keyboard event interference
    time.sleep(0.1)
    clear_input_buffer()
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username, password


