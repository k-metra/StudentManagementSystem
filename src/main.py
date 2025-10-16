import os

from utils.clear_console import clear_console
from classes.UserChoiceManager import UserChoiceManager
from utils.options import options
from termcolor import colored

def main():
    user_options = options("Login", "Exit")
    UCM = UserChoiceManager(user_options, prompt=colored("<== Student Records Management System ==>\n", "cyan", attrs=["bold"]))

    choice = UCM.get_user_choice()

    if choice == 1:
        print(colored("Exiting the program. Goodbye!", "yellow"))
        return
    elif choice == 2:
        print(colored("Login functionality is not yet implemented.", "red"))
        return

main()
