from classes.Role import Role
from enums.permissions import Permissions

class Faculty(Role):
    def __init__(self):
        super().__init__(permissions=[])