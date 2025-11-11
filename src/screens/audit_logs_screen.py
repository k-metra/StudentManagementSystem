

from termcolor import colored
from classes.Account import Account
from classes.AccountManager import AccountManager
from controllers.AuditLogController import AuditLogController
from utils.clear_console import clear_console
from utils.misc import enter_to_continue
from enums.permissions import Permissions
from utils.table_interaction import interactive_table

def audit_logs_screen(current_account: Account, account_manager: AccountManager) -> None:

    if not current_account.has_permission(Permissions.VIEW_AUDIT_LOGS):
        print(colored("\nYou do not have permission to view audit logs.", "red"))
        
        enter_to_continue()
        return

    header = colored(f"<== Audit Logs ==>", "cyan", attrs=["bold"])
    controller = AuditLogController()

    def get_audit_logs():
        logs = []

        for log_id, log_data in controller.get_all_logs().items():
            logs.append(
                {
                    "action": log_data["action"],
                    "performed_by": log_data["performed_by"],
                    "application_name": log_data["application_name"],
                    "object_id": log_data["object_id"],
                    "role": log_data["role"],
                    "date": log_data["date"]
                }
            )

        return logs

    while True:
        clear_console()

        print(header + "\n")
        audit_logs = get_audit_logs()

        columns = {
            "action": "Action",
            "performed_by": "User",
            "application_name": "Application",
            "object_id": "Object ID",
            "role": "Role",
            "date": "Date"
        }

        result = interactive_table(
                    data=audit_logs,
                    columns=columns,
                    title="Audit Logs",
                    items_per_page=15
                )
        
        if result is None:
            return
        
