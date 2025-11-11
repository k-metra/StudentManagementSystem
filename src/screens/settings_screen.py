
from utils.clear_console import clear_console 
from termcolor import colored 
from classes.UserChoiceManager import UserChoiceManager
from classes.AccountManager import AccountManager
from classes.Account import Account 
from controllers import SettingsController
from utils.misc import enter_to_continue
import pwinput

from utils.passwords import check_password, make_password

def settings_screen(current_account: Account, choice_manager: UserChoiceManager, account_manager: AccountManager) -> None:
    clear_console()

    choice_manager.set_prompt(colored(f"<== Settings ==>", "cyan", attrs=["bold"]))
    options = [
        "View Account Details",
        "Change Password",
        "Back to Main Menu"
    ]

    choice_manager.set_options(options)

    controller = SettingsController(current_account=current_account, account_manager=account_manager)


    while True:
        clear_console()
        choice = choice_manager.get_user_choice()

        match choice.label():
            case "View Account Details":
                clear_console()
                print(colored(f"<== Account Details for {current_account} ==>", "cyan", attrs=["bold"]))
                print(colored("Username: ", "cyan", attrs=["bold"]), current_account.username)
                print(colored("Role: ", "cyan", attrs=["bold"]), current_account.role)
                print(colored("Permissions: ", "cyan", attrs=["bold"]), [perm.name for perm in current_account.get_permissions()])
                enter_to_continue()
                continue
            
            case "Change Password":
                clear_console()
                current_password = pwinput.pwinput("Enter current password: ")

                if not check_password(plain_text_password=current_password, hashed_password=current_account.password):
                    print(colored("Incorrect password.", "red"))
                    enter_to_continue()
                    continue

                new_password = pwinput.pwinput("Enter new password: ")

                if len(new_password) < 6:
                    print(colored("Password must be at least 6 characters long.", "red"))
                    enter_to_continue()
                    continue

                confirm_password = pwinput.pwinput("Re-enter new password: ")

                if new_password != confirm_password:
                    print(colored("Passwords do not match.", "red"))
                    enter_to_continue()
                    continue

                success = controller.update_password(new_password)

                if success.get('status'):
                    current_account.password = new_password
                    print(colored(success.get('message'), "green"))
                else:
                    print(colored(success.get('error'), "red"))

                enter_to_continue()
                continue

            case "Back to Main Menu":
                return