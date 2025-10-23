
from controllers import ManageAccountsController
from utils.clear_console import clear_console
from classes.AccountManager import AccountManager
from classes.Account import Account
from classes.UserChoiceManager import UserChoiceManager
from utils.misc import enter_to_continue
from utils.misc import clear_input_buffer
from termcolor import colored
import pwinput

import time


def manage_accounts_screen(current_account: Account, choice_manager: UserChoiceManager) -> None:
    header = colored(f"<== Manage Accounts ==>", "cyan", attrs=["bold"])

    user_accounts = []

    controller = ManageAccountsController(current_account=current_account)

    def refresh_user_accounts():
        nonlocal user_accounts
        user_accounts = []

        # If there have been no changes, no need to refresh our array
        controller.refresh_accounts()
        if len(controller.get_all_accounts()) == len(user_accounts):
            return

        controller.refresh_accounts()

        for user_account, data in controller.get_all_accounts().items():
            user_accounts.append(
                {
                    # Format: id: number, username: string, data: dict { password: string, role: string }
                    "id": len(user_accounts) + 1,
                    "username": user_account,
                    "data": data
                }
            )
    
    refresh_user_accounts()

    while True:
        clear_console()
        line = "Account ID".ljust(12) + "Username".ljust(20) + "Role".ljust(15)

        prompt = colored(line, "white", attrs=["bold"])
        prompt += "\n" + ("-" * (12 + 20 + 15)) + "\n"

        refresh_user_accounts()
        for user_account in user_accounts:
            user_id = str(user_account.get("id"))
            username = user_account.get("username")
            role = user_account.get("data").get("role")

            account_line = user_id.ljust(12) + username.ljust(20) + role.ljust(15)

            prompt += account_line + "\n"

        
        choice_manager.set_prompt(new_prompt=prompt)
        choice_manager.set_options([
            "Create New Account",
            "Manage Existing Account",
            "Back to Main Menu"
        ])

        choice = choice_manager.get_user_choice()

        match choice.label():
            case "Back to Main Menu":
                return
            case "Create New Account":
                username = input("Enter new username: ")
                password = pwinput.pwinput("Enter new password: ")
                role = input("Enter role for the new account: ")
                result = controller.create_account(username=username, password=password, role_name=role)

                if result.get("status"):
                    print(colored(result.get("message"), "green"))
                    enter_to_continue()
                    continue 
            case "Manage Existing Account":
                user_id = input("\nEnter the Account ID to manage (0 to cancel): ")

                try:
                    user_id = int(user_id)
                except ValueError:
                    print(colored("Invalid input. Please enter a valid Account ID.", "red"))
                    enter_to_continue()
                    continue

                if user_id == 0:
                    continue
                else:
                    if user_id < 1 or user_id > len(user_accounts):
                        print(colored("Invalid Account ID. Please try again.", "red"))
                        enter_to_continue()
                        continue

                selected_account = user_accounts[user_id - 1]

                while True:
                    user_choice_manager = UserChoiceManager()

                    prompts = [
                        colored(f"<== Managing Account: {selected_account.get('username')} ==>", "cyan", attrs=["bold"]),
                        colored(f"Account ID:", "cyan", attrs=["bold"]) + colored(f" {selected_account.get('id')}", "white", attrs=[]),
                            colored(f"Username:", "cyan", attrs=["bold"]) + colored(f" {selected_account.get('username')}", "white", attrs=[]),
                    colored(f"Role:", "cyan", attrs=["bold"]) + colored(f" {selected_account.get('data').get('role')}", "white", attrs=[]),
                ]
                
                    new_prompt = "\n".join(prompts)
                    user_choice_manager.set_prompt(new_prompt)
                    user_choice_manager.set_options([
                        "Change Password",
                        "Change Role",
                        "Delete Account",
                        "Back to Account List"
                    ])

                    choice = user_choice_manager.get_user_choice()

                    match choice.label():
                        case "Change Password":
                            new_password = input("Enter new password: ")
                            result = controller.update_account(username=selected_account.get("username"), password=new_password)

                            if result.get("status"):
                                print(colored(result.get("message"), "green"))
                            else:
                                print(colored(result.get("error"), "red"))
                            enter_to_continue()

                        case "Change Role":
                            new_role = input("Enter new role: ")
                            result = controller.update_account(username=selected_account.get("username"), role_name=new_role)
                            if result.get("status"):
                                print(colored(result.get("message"), "green"))
                            else:
                                print(colored(result.get("error"), "red"))
                            enter_to_continue()

                        case "Delete Account":
                            confirm = input("Are you sure you want to delete this account? (y/n): ")
                            if confirm.lower() == "y":
                                result = controller.delete_account(username=selected_account.get("username"))
                                if result.get("status"):
                                    print(colored(result.get("message"), "green"))
                                else:
                                    print(colored(result.get("error"), "red"))
                                enter_to_continue()

                        case "Back to Account List":
                            break
