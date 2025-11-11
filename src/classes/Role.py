class Role():
    registry = {} # A registry to hold all role subclasses
    
    def __init_subclass__(cls, **kwargs):
        # Automatically register role subclasses by their names into the registry
        # for easier lookup later.
        super().__init_subclass__(**kwargs)
        Role.registry[cls.__name__] = cls

    def __init__(self, name=None, permissions=None, level: int = 0):
        self.name = name or self.__class__.__name__
        self.permissions = permissions or []
        self.level = level

    def has_permission(self, permission):
        return permission in self.permissions
    
    def __str__(self):
        return self.name