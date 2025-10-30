from classes.AccountManager import AccountManager 
from classes.Account import Account
from utils.clear_console import clear_console
from termcolor import colored 
from classes.UserChoiceManager import UserChoiceManager

def entry_screen(account_manager: AccountManager) -> Account | None:
    choice_manager = UserChoiceManager(prompt=colored("== Student Records Management System ==\n", "cyan", attrs=["bold"]))

    choice_manager.set_options([
        "Login",
        "Exit",
    ])

    while True:
        choice = choice_manager.get_user_choice()

        match choice.label():
            case "Exit":
                print(colored("\nAre you sure you want to exit the application? (Y/N)", "yellow"), end=" ")
                confirm = input().strip().lower()

                if confirm == "y":
                    print(colored("\nExiting the application. Goodbye!", "yellow"))
                    return 
                else:
                    continue
            case "Login":
                from screens import login_screen

                # Refresh account data in case of any changes
                account_manager.refresh_accounts()

                account: Account | None = login_screen(account_manager)
                
                if account is None: 
                    continue

                return account