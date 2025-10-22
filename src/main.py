import os

from utils.clear_console import clear_console
from classes.UserChoiceManager import UserChoiceManager
from utils.options import options
from termcolor import colored
from utils.login import prompt_login
from utils.file import load_file

def main():

    # Fetch accounts on startup only once after startup for performance
    accounts = load_accounts()

    user_options = options("Login", "Exit")
    UCM = UserChoiceManager(user_options, prompt=colored("<== Student Records Management System ==>\n", "cyan", attrs=["bold"]))

    option = UCM.get_user_choice()

    if option.index == 1:
        print(colored("Exiting the program. Goodbye!", "yellow"))


        return
    elif option.index == 0:
        clear_console()
        print(colored("== Login Page ==\n", "cyan", attrs=["bold"]))
        username, password = prompt_login()

        for acc in accounts:
            if acc["username"] == username and acc["password"] == password:
                print(colored(f"\nLogin successful! Welcome, {acc['role']}.", "green"))
                return
        
        print(colored("\nInvalid username or password. Please try again.", "red"))
        return
    
def load_accounts():
    return load_file("src/data/accounts.json", key="accounts")

main()
