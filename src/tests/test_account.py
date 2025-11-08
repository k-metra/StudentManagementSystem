from classes.Account import Account
from classes.Role import Role
from enums.permissions import Permissions 

def test_has_permission_true():
    role = Role(permissions=[Permissions.VIEW_REPORTS])
    account = Account(username="test", password="pass", role=role)

    assert account.has_permission(Permissions.VIEW_REPORTS) is True

def test_has_permission_false():
    role = Role(permissions=[])
    account = Account(username="test", password="pass", role=role)

    assert account.has_permission(Permissions.VIEW_REPORTS) is False

def test_str_returns_username():
    role = Role()
    account = Account(username="testuser", password="pass", role=role)
    assert str(account) == "testuser"

