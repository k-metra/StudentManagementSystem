import os

from utils.clear_console import clear_console
from classes.UserChoiceManager import UserChoiceManager
from utils.options import options
from termcolor import colored
from utils.login import prompt_login
from utils.file import load_file
from utils.misc import enter_to_continue

from classes.Account import Account

def main() -> None:

    # Fetch accounts on startup only once after startup for performance
    accounts = load_accounts()

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

                    if username not in accounts:
                        print(colored("\nNo account found with that username.", "red"))
                        enter_to_continue()
                        continue 

                    if accounts[username]["password"] != password:
                        print(colored("\nInvalid password. Please try again.", "red"))
                        enter_to_continue()
                        continue
                    
                    current_account = Account(username=username, password=password, role=accounts[username]["role"])

                    print(colored(f"\nLogin successful! Welcome, {current_account}.", "green"))
                    enter_to_continue()
                    continue

        # If user is logged in
        else:
            UCM.set_prompt(colored(f"<== Welcome, {current_account}! ==>","cyan", attrs=["bold"]))
            menu = options(
                "View Students",
                "Add Student",
                "Remove Student",
                "Logout"
            )
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
    
def load_accounts():
    return load_file("src/data/accounts.json", key="accounts")

main()
