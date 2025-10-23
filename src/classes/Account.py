from .Role import Role

class Account():
    def __init__(self, username: str, password: str, role: Role):
        self.username = username
        self.password = password
        self.role = role

    def has_permission(self, permission):
        return (permission in self.role.permissions)
    
    def __str__(self):
        return self.username