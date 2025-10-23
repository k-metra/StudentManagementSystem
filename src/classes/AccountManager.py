from utils.file import load_file
from classes.Account import Account
from classes.Role import Role
import roles 
import pkgutil as package_utils

class AccountManager:
    def __init__(self):
        self._accounts = None 
        self._role_registry = None

        # Dynamically import all roles in the Roles package
        # so that they are registered into the role registry
        for _, name, _ in package_utils.iter_modules(roles.__path__):
            __import__(f"roles.{name}")
        
        self._role_registry = Role.registry

    def load_accounts(self) -> dict[str, dict]:
        if self._accounts is None:
            self._accounts = load_file("src/data/accounts.json", key="accounts")
        
        return self._accounts
    
    def get_account(self, username: str, password: str, role: str | None = None) -> dict[str, str] | None:
        if self._accounts is None:
            self.load_accounts()
        
        if username not in self._accounts:
            return None 
        
        if password != self._accounts[username]["password"]:
            return None 
        
        if role and self._accounts[username]["role"] != role:
            return None 
        
        if role and role not in self._role_registry:
            raise ValueError(f"Role '{role}' is not a valid role.")

        return self._accounts[username]
    

    # This has no validation and is only for parsing account data into an actual 'Account' object
    # For validation, use get_account() first, which returns parsable account data
    def load_account(self, username: str, account_json: dict[str, str]) -> Account:
        account_role = self._role_registry[account_json.get("role")]

        return Account(username=username, password=account_json.get("password"), role=account_role())