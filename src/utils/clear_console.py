import os

# Small helper function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Based on the operating system
    # For windows it uses 'cls'
    # For mac and linux it uses 'clear'