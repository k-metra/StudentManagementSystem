from classes.Role import Role
from enums.permissions import Permissions

class Registrar(Role):
    def __init__(self):
        super().__init__(permissions=[
            Permissions.ADD_STUDENT,
            Permissions.EDIT_STUDENT,
            Permissions.DELETE_STUDENT,
            Permissions.VIEW_REPORTS,
        ])  