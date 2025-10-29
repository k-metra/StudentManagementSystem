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

from screens import login_screen


def main() -> None:
    account_manager = AccountManager()
    current_account: Account | None = None

    while True:
        if current_account is None:
            from screens import entry_screen

            # "entry_screen" will either return:
            # An account if the user logs in
            # 'None' if the user chooses to exit the application
            current_account = entry_screen(account_manager)

            if current_account is None:
                break

            continue
        

        from screens import main_menu_screen
        main_menu_screen(current_account, account_manager)
        current_account = None


main()

