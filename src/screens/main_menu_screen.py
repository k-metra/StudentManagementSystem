from utils.options import options 
from utils.clear_console import clear_console
from termcolor import colored
from classes.UserChoiceManager import UserChoiceManager
from enums.permissions import Permissions
from utils.misc import enter_to_continue
from classes.Account import Account

def main_menu_screen(current_account: Account) -> None:
    manager = UserChoiceManager()

    while True:
        clear_console()
        manager.set_prompt(colored(f"<== Welcome, {current_account}! ==>", "cyan", attrs=["bold"]))

        menu_options = [
            "View Students",
            "Add Student",
            "Remove Student"
        ]

        if current_account.has_permission(Permissions.EDIT_ACCOUNT):
            menu_options.append("Manage Accounts")
        
        menu_options.append("Logout")
        manager.set_options(menu_options)
        choice = manager.get_user_choice()

        match choice.label():
            case "Logout":
                print("Logging out...")
                enter_to_continue()
        
                return
            case "Manage Accounts":
                # Manage accounts screen logic here
                pass 
            case other:
                print(f"You selected: {other}")
                enter_to_continue()