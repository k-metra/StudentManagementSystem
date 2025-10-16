from classes import Role
from enums.permissions import Permissions

class Staff(Role):
    def __init__(self):
        permissions = [
            Permissions.ADD_STUDENT,
            Permissions.EDIT_STUDENT,
        ]