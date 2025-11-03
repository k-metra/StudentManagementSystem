from classes.Role import Role
from enums.permissions import Permissions

class Staff(Role):
    def __init__(self):
        super().__init__(permissions=[
            Permissions.ADD_STUDENT,
            #Permissions.EDIT_STUDENT,
        ])