import json
import tempfile
from controllers.ManageAccountsController import ManageAccountsController
from classes.Account import Account
from classes.Role import Role 
from enums.permissions import Permissions

def test_create_account_success(monkeypatch):
    role = Role(name="User", permissions=[Permissions.CREATE_ACCOUNT])
    admin = Account("admin", "pass", role)
    controller = ManageAccountsController(admin)

    controller.accounts = {}
    controller.account_manager._role_registry = {"Admin": Role}
    
    monkeypatch.setattr(controller, "save_accounts", lambda: None)

    result = controller.create_account("newuser", "newpass", "Admin")
    assert result["status"] is True 

def test_create_account_existing_user(monkeypatch):
    role = Role("Admin", permissions=[Permissions.CREATE_ACCOUNT])

    admin = Account("admin", "pass", role)

    controller = ManageAccountsController(admin)
    controller.accounts = {"newuser": {"password": "123", "role": "Admin"}}
    controller.account_manager._role_registry = {"Admin": Role}
    monkeypatch.setattr(controller, "save_accounts", lambda: None)

    result = controller.create_account("newuser", "newpass", "Admin")
    assert result["status"] is False

def test_create_account_fail(monkeypatch):
    role = Role(name="User", permissions=[])
    account = Account("UserAccount", "pass", role=role)
    controller = ManageAccountsController(account)

    controller.accounts = {}
    controller.account_manager._role_registry = {"User": Role}

    monkeypatch.setattr(controller, "save_accounts", lambda: None)

    result = controller.create_account("newuser", "newpass", "Admin")
    assert result["status"] is False

def test_delete_account_fail(staff_account):
    controller = ManageAccountsController(staff_account)
    controller.accounts = {"user1": {"password": "123", "role": "Staff"}}

    result = controller.delete_account("nonexistentuser")
    assert result["status"] is False