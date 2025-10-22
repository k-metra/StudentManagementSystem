import os

from utils.clear_console import clear_console
from classes.UserChoiceManager import UserChoiceManager
from utils.options import options
from termcolor import colored
from utils.login import access_file, prompt_login, load_accounts


def main():

    user_options = options("Login", "Exit")
    UCM = UserChoiceManager(user_options, prompt=colored("<== Student Records Management System ==>\n", "cyan", attrs=["bold"]))
    open_file = access_file("src/data/accounts.json")
    option = UCM.get_user_choice()

    if option.index == 1:
        print(colored("Exiting the program. Goodbye!", "yellow"))


        return
    elif option.index == 0:
        clear_console()
        print(colored("== Login Page ==\n", "cyan", attrs=["bold"]))
        accounts = load_accounts("src/data/accounts.json")
        username, password = prompt_login()

        for acc in accounts:
            if acc["username"] == username and acc["password"] == password:
                print(colored(f"\nLogin successful! Welcome, {acc['role']}.", "green"))
                return
        
        print(colored("\nInvalid username or password. Please try again.", "red"))
        return
main()
