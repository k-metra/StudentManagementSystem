class Role():
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions

    def has_permission(self, permission):
        return permission in self.permissions