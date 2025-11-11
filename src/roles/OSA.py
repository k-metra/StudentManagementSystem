from classes.Role import Role
from enums.permissions import Permissions

class OSA(Role):
    def __init__(self):
        super().__init__(name="Office of Student Affairs", permissions=[
            Permissions.VIEW_REPORTS,
            Permissions.ADD_STUDENT,
            Permissions.EDIT_STUDENT,
        ], level=7)  