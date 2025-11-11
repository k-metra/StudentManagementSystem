from classes.Role import Role
from enums.permissions import Permissions

class ITM(Role):
    def __init__(self):
        super().__init__(permissions=[
            Permissions.ADD_STUDENT,
            Permissions.EDIT_STUDENT,
            Permissions.DELETE_STUDENT,
            Permissions.VIEW_REPORTS,
            Permissions.CREATE_ACCOUNT,
            Permissions.EDIT_ACCOUNT,
            Permissions.DELETE_ACCOUNT,
            Permissions.VIEW_AUDIT_LOGS,
        ])  