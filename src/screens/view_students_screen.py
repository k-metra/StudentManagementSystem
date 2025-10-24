from controllers import ManageStudentsController
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
        controller.refresh_students()
        if len(controller.get_all_students()) == len(student_records):
            return

        for student_id, data in controller.get_all_students().items():
            student_records.append(
                {
                    # Format: id: number, student_id: string, data: dict { first_name: string, last_name: string, phone_number: string, year_level: int, course: string }
                    "id": len(student_records) + 1,
                    "student_id": student_id,
                    "data": data
                }
            )
        refesh_student_records()

        while True:
            clear_console()
            line = "Record ID".ljust(12) + "Student ID".ljust(15) + "Name".ljust(25) + "Year Level".ljust(12) + "Course".ljust(20)

            prompt = colored(line, "white", attrs=["bold"])
            prompt += "\n" + ("-" * (12 + 15 + 25 + 12 + 20)) + "\n"
            refresh_student_records()
            for student_record in student_records:
                record_id = str(student_record.get("id"))
                student_id = student_record.get("student_id")
                data = student_record.get("data")
                name = f"{data.get('first_name')} {data.get('last_name')}"
                year_level = str(data.get("year_level"))
                course = data.get("course")

                record_line = record_id.ljust(12) + student_id.ljust(15) + name.ljust(25) + year_level.ljust(12) + course.ljust(20)

                prompt += record_line + "\n"

            choice_manager.set_prompt(new_prompt=prompt)
            choice_manager.set_options([
                "Create New Account",
                "Manage Existing Account",
                "Back to Main Menu"
            ])
