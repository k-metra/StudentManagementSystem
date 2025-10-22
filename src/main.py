import os

from utils.clear_console import clear_console
from classes.UserChoiceManager import UserChoiceManager
from utils.options import options
from termcolor import colored
from utils.login import prompt_login
from utils.file import load_file

def main() -> None:

    # Fetch accounts on startup only once after startup for performance
    accounts = load_accounts()

    user_options = options("Login", "Exit")
    UCM = UserChoiceManager(user_options, prompt=colored("<== Student Records Management System ==>\n", "cyan", attrs=["bold"]))

    option = UCM.get_user_choice()

    match option.label():
        case "Exit":
            print(colored("Exiting the program. Goodbye!", "yellow"))
            return 
        case "Login":
            clear_console()
            print(colored("== Login Page ==\n", "cyan", attrs=["bold"]))
            username, password = prompt_login()


            # Instead of running a loop, we just check once if the username exists and if the password matches.
            if username not in accounts:
                print(colored("\nNo account found with that username.", "red"))
                return
            
            if accounts[username]["password"] != password:
                print(colored("\nInvalid password. Please try again.", "red"))
                return

            print(colored(f"\nLogin successful! Welcome, {accounts[username]['role']}.", "green"))
            return 
        
        case _:
            print(colored("An unknown error occurred.", "red"))
            return
    
def load_accounts():
    return load_file("src/data/accounts.json", key="accounts")

main()
