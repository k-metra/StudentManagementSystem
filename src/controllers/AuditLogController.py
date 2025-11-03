from datetime import datetime
import json
from dotenv import load_dotenv

from classes.Account import Account

import os

from termcolor import colored

from classes.Role import Role
from utils.misc import enter_to_continue

class AuditLogController():
    def __init__(self):
        self.logs = []
        load_dotenv()
        self.DATA_FILE = os.getenv("AUDIT_LOG_DATA_FILE")

    def get_all_logs(self) -> list[dict]:
        return self.logs
    
    def save_logs(self) -> None:
        try:
            with open(self.DATA_FILE, "w", encoding="utf-8") as file:
                json.dump({"logs": self.logs}, file, indent=4, default=str)
        
        except FileNotFoundError:
            print(colored("Something went wrong with trying to save audit logs. File not found.", "red"))
            enter_to_continue()
            return 
        
        if os.getenv("DEBUG").lower() == "true":
            print(colored("Audit logs saved successfully.", "green"))
            enter_to_continue()

    
    def add_log(self, action: str, performed_by: str | Account, application_name: str, date: datetime | None = datetime.now(), role: str | None | Role = None ) -> None:
        '''
            Inserts a new log into audit logs.

            Parameters:
                action (str): Name of the action (create, update, delete)
                performed_by (str | Account): Username or Account object of the user who performed the action
                role (str | Role, optional): Role name or Role object of the user who performed the action
                application_name (str): Name of the application (Students, Accounts, etc)
                date (datetime, optional): Date and time of the action. Defaults to current date and time.
        '''

        if isinstance(performed_by, Account):
            performed_by = performed_by.username
        
        if isinstance(role, Role):
            role = role.name
        elif role is None and isinstance(performed_by, Account):
            role = performed_by.role.name
        else:
            role = "Unknown (parsing error)"

        log_entry = {
            "action": action,
            "performed_by": performed_by,
            "application_name": application_name,
            "role": role,
            "date": date
        }

        if os.getenv("DEBUG").lower() == "true":
            print(colored(f"Adding audit log: {log_entry}", "yellow"))
            enter_to_continue()

        self.logs.append(log_entry)
        self.save_logs()
