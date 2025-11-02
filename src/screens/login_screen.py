from utils.clear_console import clear_console
from utils.login import prompt_login
from utils.misc import enter_to_continue
from termcolor import colored
from classes.AccountManager import AccountManager
from classes.Account import Account
from utils.passwords import check_password

def login_screen(account_manager: AccountManager) -> Account | None:
    while True:
        clear_console()
        print(colored("== Login Page ==\n", "cyan", attrs=["bold"]))
        print("Input blank username and password to exit.\n")

        username, password = prompt_login()

        if not username and not password:
            return None

        account_data: Account = account_manager.get_account(username=username)
        if account_data is None:
            print(colored(f"\nAccount with username '{username}' does not exist.", "red"))
            enter_to_continue()
            continue 

        if not check_password(password, account_data.get("password", "")):
            print(colored("\nIncorrect password. Please try again.", "red"))
            enter_to_continue()
            continue

        account: Account = account_manager.load_account(username=username, account_json=account_data)
        print(colored(f"\nLogin successful! Welcome, {account}.", "green"))
        enter_to_continue()
        return account