from classes import Role
from enums.permissions import Permissions

class Admin(Role):
    def __init__(self):
        self.permissions = [
            Permissions.ADD_STUDENT,
            Permissions.EDIT_STUDENT,
            Permissions.DELETE_STUDENT,
            Permissions.VIEW_REPORTS,
            Permissions.CREATE_ACCOUNT,
            Permissions.EDIT_ACCOUNT,
        ]