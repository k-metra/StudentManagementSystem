import os

from utils.clear_console import clear_console
from classes.UserChoiceManager import UserChoiceManager
from utils.options import options
from termcolor import colored
from utils.login import access_file


def main():
    user_options = options("Login", "Exit")
    UCM = UserChoiceManager(user_options, prompt=colored("<== Student Records Management System ==>\n", "cyan", attrs=["bold"]))
    open_file = access_file("src/data/accounts.json")
    choice = UCM.get_user_choice()

<<<<<<< HEAD
    match str(choice):
        case "Exit":
            print(colored("Exiting the program. Goodbye!", "yellow"))
            return
        case "Login":
            print(colored("Login functionality is not yet implemented.", "red"))
            return

=======
    if choice == 1:
        print(colored("Exiting the program. Goodbye!", "yellow"))
        
        return
    elif choice == 0:
        print(open_file)
        
        print(colored("Login functionality is not yet implemented.", "red"))
        
        return
>>>>>>> will(login_attempt)
main()
