from classes.Role import Role
from enums.permissions import Permissions

class OAA(Role):
    def __init__(self):
        super().__init__(name="Office of Academic Affairs", permissions=[  
            Permissions.VIEW_REPORTS,
            Permissions.ADD_STUDENT,
            Permissions.EDIT_STUDENT,
        ], level=7)  