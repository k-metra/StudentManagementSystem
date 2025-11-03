from enum import IntFlag, auto

class Permissions(IntFlag):
    ADD_STUDENT = auto()
    DELETE_STUDENT = auto()
    EDIT_STUDENT = auto()
    CREATE_ACCOUNT = auto()
    DELETE_ACCOUNT = auto()
    EDIT_ACCOUNT = auto()
    VIEW_REPORTS = auto()
    VIEW_AUDIT_LOGS = auto()