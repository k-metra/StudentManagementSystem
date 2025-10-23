from .file import load_file
from classes.Account import Account
from classes.Role import Role
import roles 
import pkgutil as package_utils

# Dynamically import all roles in the roles package
# so that they are registered in the roles module namespace
for finder, name, is_package in package_utils.iter_modules(roles.__path__):
    __import__(f"roles.{name}")

# after dynamic import, registry will have all roles automatically
roles_registry = Role.registry

global accounts
accounts = None

def get_account(username: str, password: str, role: str="") -> dict[str, str] | None:
    global accounts 
    if accounts is None:
        accounts = load_accounts()
    
    if username not in accounts:
        return None 
    
    if password and accounts[username]["password"] != password:
        return None
    
    if role and accounts[username]["role"] != role:
        return None
    
    return accounts[username]
    

def load_accounts() -> dict[str, dict]:
    return load_file("src/data/accounts.json", key="accounts")

def load_account(username: str, password: str, role: str) -> Account:
    if role not in roles_registry:
        raise ValueError(f"Role '{role}' does not exist.")
    
    if username not in accounts:
        raise ValueError(f"Account with username '{username}' does not exist.")

    if password and accounts[username]["password"] != password:
        raise ValueError("Invalid password.")

    if role and accounts[username]["role"] != role:
        raise ValueError("Invalid role.")

    return Account(username=username, password=password, role=roles_registry[role]())
