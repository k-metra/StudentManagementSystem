import pytest
from classes.Role import Role 
from classes.Account import Account
from enums.permissions import Permissions

@pytest.fixture
def admin_role():
    class Admin(Role):
        def __init__(self):
            super().__init__(name="Admin", permissions=[
                Permissions.ADD_STUDENT,
                Permissions.CREATE_ACCOUNT,
                Permissions.DELETE_ACCOUNT,
                Permissions.DELETE_STUDENT,
                Permissions.VIEW_AUDIT_LOGS,
                Permissions.EDIT_ACCOUNT,
                Permissions.EDIT_STUDENT,
                Permissions.VIEW_REPORTS
            ])

@pytest.fixture
def admin_account(admin_role):
    return Account(username="admin", password="adminpass", role=admin_role)