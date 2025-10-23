from classes.AccountManager import AccountManager
from classes.Account import Account 
from enums.permissions import Permissions
from roles import * # Import all roles
from dotenv import load_dotenv
import os
import json 

class ManageAccountsController:

    def __init__(self, current_account: Account):
        self.account_manager = AccountManager()
        self.accounts = self.account_manager.load_accounts()
        self.current_account = current_account

        load_dotenv()

        self.DATA_FILE = os.getenv("ACCOUNTS_DATA_FILE")

    # ---------------
    # Utility Helpers
    # ---------------

    def refresh_accounts(self):
        self.account_manager.refresh_accounts()
        self.accounts = self.account_manager.load_accounts()

    # Writes the current account data back to the JSON file
    def save_accounts(self):
        with open(self.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump({"accounts": self.accounts}, file, indent=4)

    # ---------------
    # CRUD Operations
    # ---------------

    def get_all_accounts(self) -> dict[str, dict]:
        return self.accounts 
    
    def create_account(self, username: str, password: str, role_name: str) -> dict[str, str | bool]:
        if username in self.accounts:
            return {"status": False, "error" : "Account with that username already exists."}
        
        if role_name not in self.account_manager._role_registry:
            return {"status": False, "error" : "Role does not exist."}
        
        self.accounts[username] = {
            "password": password,
            "role": role_name
        }

        self.save_accounts()
        return {"status": True, "message": f"Account '{username}' created successfully."}
    
    def delete_account(self, username: str) -> dict[str, str | bool]:
        if username not in self.accounts:
            return {"status": False, "error":"No account with that username exists."}
        
        if username == self.current_account.username:
            return {"status": False, "error":"You cannot delete your own account while logged in."}
        
        if not self.current_account.has_permission(Permissions.DELETE_ACCOUNT):
            return {"status": False, "error":"You do not have permission to delete accounts."}
        
        del self.accounts[username]
        self.save_accounts()
        return {"status": True, "message": f"Account '{username}' deleted successfully."}
    
    def update_account(self, username: str, password: str | None = None, role_name: str | None = None) -> dict[str, str | bool]:
        if username == self.current_account.username:
            return {"status": False, "error":"You cannot edit your own account while logged in."}

        if username not in self.accounts:
            return {"status": False, "error":"No account with that username exists."}
        
        if not self.current_account.has_permission(Permissions.EDIT_ACCOUNT):
            return {"status": False, "error":"You do not have permission to edit accounts."}
        
        if password:
            if len(password) < 6:
                return {"status": False, "error":"Password must be at least 6 characters long."}
            self.accounts[username]["password"] = password 
        
        if role_name:
            if role_name not in self.account_manager._role_registry:
                return {"status": False, "error":f"Role {role_name} does not exist."}
            self.accounts[username]["role"] = role_name

        
        self.save_accounts()
        return {"status": True, "message": f"Account '{username}' updated successfully.\n"}