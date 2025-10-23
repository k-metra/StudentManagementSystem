class Role():
    registry = {} # A registry to hold all role subclasses
    
    def __init_subclass__(cls, **kwargs):
        # Automatically register role subclasses by their names into the registry
        # for easier lookup later.
        super().__init_subclass__(**kwargs)
        Role.registry[cls.__name__] = cls

    def __init__(self, name=None, permissions=None):
        self.name = name or self.__class__.__name__
        self.permissions = permissions or []

    def has_permission(self, permission):
        return permission in self.permissions