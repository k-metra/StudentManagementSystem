from classes.Role import Role
from enums.permissions import Permissions

class CollegeDean(Role):
    def __init__(self):
        super().__init__(name="College Dean", permissions=[
            Permissions.ADD_STUDENT,
            Permissions.EDIT_STUDENT,
            Permissions.DELETE_STUDENT,
            Permissions.VIEW_REPORTS,
            Permissions.CREATE_ACCOUNT,
        ], level=7)  