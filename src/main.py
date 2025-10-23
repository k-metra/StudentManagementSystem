import os

from utils.clear_console import clear_console
from classes.UserChoiceManager import UserChoiceManager
from utils.options import options
from termcolor import colored
from utils.login import prompt_login
from utils.file import load_file
from utils.misc import enter_to_continue

from classes.Account import Account
import utils.account_utils as account_utils
from roles import * # Imports all the roles inside the roles package

from enums.permissions import Permissions

def main() -> None:
    initial_options = options("Login", "Exit")
    UCM = UserChoiceManager()

    current_account: Account | None = None

    while True:
        # If user is logged out or not logged in
        if current_account is None:
            UCM.set_options(initial_options)
            UCM.set_prompt(colored("<== Student Management System ==>","cyan", attrs=["bold"]))

            choice = UCM.get_user_choice()

            match choice.label():
                case "Exit":
                    print(colored("Exiting the program. Goodbye!", "yellow"))
                    break

                case "Login":
                    clear_console()
                    print(colored("== Login Page ==\n", "cyan", attrs=["bold"]))
                    username, password = prompt_login()

                    account = account_utils.get_account(username=username, password=password)

                    if account is None:
                        print(colored("\nInvalid username or password. Please try again.", "red"))
                        enter_to_continue()
                        continue
                    
                    current_account = account_utils.load_account(username=username, password=account.get("password"), role=account.get("role"))

                    print(colored(f"\nLogin successful! Welcome, {current_account}.", "green"))
                    enter_to_continue()
                    continue

        # If user is logged in
        else:
            UCM.set_prompt(colored(f"<== Welcome, {current_account}! ==>","cyan", attrs=["bold"]))

            # Build menu options based on user permissions
            menu_options = [
                "View Students",
                "Add Student",
                "Remove Student",
            ]

            # Add admin-only options if user has permission
            if current_account.has_permission(Permissions.EDIT_ACCOUNT):
                menu_options.append("Manage Accounts")

            # Always add logout option at the end
            menu_options.append("Logout")

            menu = options(*menu_options)
            UCM.set_options(menu)
            choice = UCM.get_user_choice()

            match choice.label():
                case "Logout":
                    print(colored(f"\nLogging out {current_account}...", "yellow"))
                    current_account = None
                    enter_to_continue()
                    continue

                case other_option:
                    print(colored(f"\nYou selected: {other_option}", "green"))
                    enter_to_continue()
                    continue
    


main()
