from controllers import ManageStudentsControllers
from utils.clear_console import clear_console
from classes.AccountManager import AccountManager
from classes.Account import Account
from classes.UserChoiceManager import UserChoiceManager
from utils.misc import enter_to_continue
from utils.misc import clear_input_buffer
from termcolor import colored

def manage_students_screen(current_account: Account, choice_manager: UserChoiceManager) -> None:
    header = colored(f"<== View Students ==>", "cyan", attrs=["bold"])

    student_records = []
    controller = ManageStudentsController(current_account=current_account)
    def refresh_student_records():
        nonlocal student_records
        student_records = []

        # If there have been no changes, no need to refresh our array
        controller.load_students()
        if len(controller.get_all_students()) == len(student_records):
            return

        for student_id, data in controller.get_all_students().items():
            student_records.append(
                {
                    "id": len(student_records) + 1,
                    "student_id": student_id,
                    "data": data
                }
            )
        refresh_student_records()


