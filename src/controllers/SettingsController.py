import os
from dotenv import load_dotenv
from classes import Account
from classes.AccountManager import AccountManager
import json

class SettingsController:

    def __init__(self, current_account: Account, account_manager: AccountManager):
        self.account_manager = account_manager
        self.current_account = current_account

        load_dotenv()
        self.DATA_FILE = os.getenv("ACCOUNTS_DATA_FILE")

    def get_account_manager(self) -> AccountManager:
        return self.account_manager
    
    def update_password(self, new_password: str) -> dict[str, str | bool]:
        accounts = self.account_manager.load_accounts()

        if self.current_account.username not in accounts:
            return {"status": False, "error": "Current account does not exist."}
        
        accounts[self.current_account.username]["password"] = new_password

        try:
            with open(self.DATA_FILE, "w", encoding="utf-8") as file:
                try:
                    json.dump({"accounts": accounts}, file, indent=4)
                except TypeError as e:
                    return {"status": False, "error": f"Failed to serialize account data: {str(e)}"}

            return {"status": True, "message": "Password updated successfully."}
        except Exception as e:
            return {"status": False, "error": str(e)}