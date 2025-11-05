from controllers import AuditLogController, ManageAccountsController
from utils.clear_console import clear_console
from classes.Account import Account
from classes.UserChoiceManager import UserChoiceManager
from utils.misc import enter_to_continue
from utils.misc import clear_input_buffer
from utils.passwords import make_password
from utils.table_interaction import interactive_table
from termcolor import colored
from enums.permissions import Permissions
import pwinput

def manage_accounts_screen(current_account: Account, choice_manager: UserChoiceManager) -> None:
    controller = ManageAccountsController(current_account=current_account)
    
    def get_accounts_data():
        """Get accounts data formatted for table display"""
        controller.refresh_accounts()
        accounts_data = []
        
        for username, data in controller.get_all_accounts().items():
            accounts_data.append({
                "username": username,
                "role": data.get("role", "Unknown"),
                "password": "••••••••"  # Hidden for security
            })
        
        return accounts_data
    
    def handle_account_selection(selected_account: dict, item_id: int):
        """Handle when an account is selected from the table"""
        manage_single_account(current_account, selected_account, controller)
    
    # Define table columns
    columns = {
        "username": "Username",
        "role": "Role",
        "password": "Password"
    }
    
    while True:
        accounts_data = get_accounts_data()
        additional_options = []

        if current_account.has_permission(Permissions.CREATE_ACCOUNT):
            additional_options.append("Create New Account")
        
        # Show interactive table
        result = interactive_table(
            data=accounts_data,
            columns=columns,
            title="Manage Accounts",
            additional_options=additional_options,
            on_select_item=handle_account_selection,
            items_per_page=10
        )
        
        if result is None:  # Back was selected
            return
        elif result == "Create New Account":
            create_new_account(current_account, controller)

def create_new_account(current_account: Account, controller):
    """Handle creating a new account"""

    if not current_account.has_permission(Permissions.CREATE_ACCOUNT):
        print(colored("You do not have permission to create new accounts.", "red"))
        enter_to_continue()
        return

    clear_console()
    print(colored("<== Create New Account ==>", "cyan", attrs=["bold"]))
    print()
    
    username = input("Enter new username: ").strip()
    if not username:
        print(colored("Username cannot be empty.", "red"))
        enter_to_continue()
        return
    
    password = pwinput.pwinput("Enter new password: ")
    if not password:
        print(colored("Password cannot be empty.", "red"))
        enter_to_continue()
        return
    
    password = make_password(password)
    
    role = input("Enter role for the new account: ").strip()
    if not role:
        print(colored("Role cannot be empty.", "red"))
        enter_to_continue()
        return
    
    result = controller.create_account(username=username, password=password, role_name=role)
    
    if result.get("status"):
        print(colored(result.get("message"), "green"))
        AuditLogController().add_log(
            action="Create Account",
            performed_by=current_account,
            application_name="Accounts",
            object_id=username,
            role=current_account.role
        )
    else:
        print(colored(result.get("error", "Failed to create account"), "red"))
    
    enter_to_continue()

def manage_single_account(current_account: Account, selected_account: dict, controller):
    """Handle managing a single account"""
    choice_manager = UserChoiceManager()
    username = selected_account["username"]
    
    while True:
        clear_console()
        
        # Refresh account data
        controller.refresh_accounts()
        all_accounts = controller.get_all_accounts()
        
        if username not in all_accounts:
            print(colored("Account no longer exists.", "red"))
            enter_to_continue()
            return
        
        account_data = all_accounts[username]
        
        prompts = [
            colored(f"<== Managing Account: {username} ==>", "cyan", attrs=["bold"]),
            "",
            colored(f"Username:", "cyan", attrs=["bold"]) + colored(f" {username}", "white"),
            colored(f"Role:", "cyan", attrs=["bold"]) + colored(f" {account_data.get('role', 'Unknown')}", "white"),
            ""
        ]
        
        prompt = "\n".join(prompts)
        
        choice_manager.set_prompt(prompt)

        options = []

        if current_account.has_permission(Permissions.EDIT_ACCOUNT):
            options.extend([
                "Change Password",
                "Change Role",
            ])

        if current_account.has_permission(Permissions.DELETE_ACCOUNT):
            options.append("Delete Account")

        options.append("Back to Account List")
        choice_manager.set_options(options)
        
        choice = choice_manager.get_user_choice()
        
        match choice.label():
            case "Change Password":
                if not current_account.has_permission(Permissions.EDIT_ACCOUNT):
                    print(colored("You do not have permission to change account passwords.", "red"))
                    enter_to_continue()
                    continue

                change_account_password(username, current_account, controller)
            case "Change Role":
                if not current_account.has_permission(Permissions.EDIT_ACCOUNT):
                    print(colored("You do not have permission to change account roles.", "red"))
                    enter_to_continue()
                    continue

                change_account_role(username, current_account, controller)
            case "Delete Account":
                if not current_account.has_permission(Permissions.DELETE_ACCOUNT):
                    print(colored("You do not have permission to delete accounts.", "red"))
                    enter_to_continue()
                    continue
                if delete_account(username, current_account, controller):
                    return  # Account deleted, go back to list
            case "Back to Account List":
                return

def change_account_password(username: str, current_account: Account, controller):
    """Handle changing account password"""
    clear_console()
    print(colored(f"<== Change Password for {username} ==>", "cyan", attrs=["bold"]))
    print()
    
    new_password = pwinput.pwinput("Enter new password: ")
    if not new_password:
        print(colored("Password cannot be empty.", "red"))
        enter_to_continue()
        return
    
    
    confirm_password = pwinput.pwinput("Re-enter new password: ")
    
    if new_password != confirm_password:
        print(colored("Passwords do not match.", "red"))
        enter_to_continue()
        return
    
    new_password = make_password(new_password)

    result = controller.update_account(username=username, password=new_password)
    
    if result.get("status"):
        print(colored(result.get("message"), "green"))
        AuditLogController().add_log(
            action="Update Password",
            performed_by=current_account,
            application_name="Accounts",
            object_id=username,
            role=current_account.role
        )
    else:
        print(colored(result.get("error", "Failed to update password"), "red"))
    
    enter_to_continue()

def change_account_role(username: str, current_account: Account, controller):
    """Handle changing account role"""
    clear_console()
    print(colored(f"<== Change Role for {username} ==>", "cyan", attrs=["bold"]))
    print()
    
    new_role = input("Enter new role: ").strip()
    if not new_role:
        print(colored("Role cannot be empty.", "red"))
        enter_to_continue()
        return
    
    result = controller.update_account(username=username, role_name=new_role)
    
    if result.get("status"):
        print(colored(result.get("message"), "green"))
        AuditLogController().add_log(
            action="Update Role",
            performed_by=current_account,
            application_name="Accounts",
            object_id=username,
            role=current_account.role
        )
    else:
        print(colored(result.get("error", "Failed to update role"), "red"))
    
    enter_to_continue()

def delete_account(username: str, current_account: Account, controller) -> bool:
    """Handle deleting account. Returns True if deleted, False otherwise"""
    clear_console()
    print(colored(f"<== Delete Account: {username} ==>", "cyan", attrs=["bold"]))
    print()
    print(colored("WARNING: This action cannot be undone!", "red", attrs=["bold"]))
    print()
    
    confirm = input("Are you sure you want to delete this account? Type 'DELETE' to confirm: ").strip()
    
    if confirm == "DELETE":
        result = controller.delete_account(username=username)
        if result.get("status"):
            print(colored(result.get("message"), "green"))
            AuditLogController().add_log(
                action="Delete Account",
                performed_by=current_account,
                application_name="Accounts",
                object_id=username,
                role=current_account.role
            )
            enter_to_continue()
            return True
        else:
            print(colored(result.get("error", "Failed to delete account"), "red"))
            enter_to_continue()
            return False
    else:
        print(colored("Account deletion cancelled.", "yellow"))
        enter_to_continue()
        return False