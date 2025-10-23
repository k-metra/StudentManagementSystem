import os

from utils.clear_console import clear_console
from classes.UserChoiceManager import UserChoiceManager
from classes.AccountManager import AccountManager
from utils.options import options
from termcolor import colored
from utils.login import prompt_login
from utils.file import load_file
from utils.misc import enter_to_continue

from classes.Account import Account
from roles import * # Imports all the roles inside the roles package

from enums.permissions import Permissions

def main() -> None:
    initial_options = options("Login", "Exit")

    # Initialize managers
    managers = {
        "Account": AccountManager(),
        "Choices": UserChoiceManager()
    }

    current_account: Account | None = None

    while True:
        # If user is logged out or not logged in
        if current_account is None:
            managers.get("Choices").set_options(initial_options)
            managers.get("Choices").set_prompt(colored("<== Student Management System ==>","cyan", attrs=["bold"]))

            choice = managers.get("Choices").get_user_choice()

            match choice.label():
                case "Exit":
                    print(colored("Exiting the program. Goodbye!", "yellow"))
                    break

                case "Login":
                    clear_console()
                    print(colored("== Login Page ==\n", "cyan", attrs=["bold"]))
                    username, password = prompt_login()

                    account = managers.get("Account").get_account(username=username, password=password)

                    if account is None:
                        print(colored("\nInvalid username or password. Please try again.", "red"))
                        enter_to_continue()
                        continue
                    
                    current_account = managers.get("Account").load_account(username=username, account_json=account)

                    print(colored(f"\nLogin successful! Welcome, {current_account}.", "green"))
                    enter_to_continue()
                    continue

        # If user is logged in
        else:
            managers.get("Choices").set_prompt(colored(f"<== Welcome, {current_account}! ==>","cyan", attrs=["bold"]))

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
            managers.get("Choices").set_options(menu)
            choice = managers.get("Choices").get_user_choice()

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
