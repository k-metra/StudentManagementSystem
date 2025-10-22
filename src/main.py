import os

from utils.clear_console import clear_console
from classes.UserChoiceManager import UserChoiceManager
from utils.options import options
from termcolor import colored

def main():
    user_options = options("Login", "Exit")
    UCM = UserChoiceManager(user_options, prompt=colored("<== Student Records Management System ==>\n", "cyan", attrs=["bold"]))

    choice = UCM.get_user_choice()

    match str(choice):
        case "Exit":
            print(colored("Exiting the program. Goodbye!", "yellow"))
            return
        case "Login":
            print(colored("Login functionality is not yet implemented.", "red"))
            return

main()
