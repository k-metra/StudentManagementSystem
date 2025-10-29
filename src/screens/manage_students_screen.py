
from controllers import ManageStudentsController
from utils.clear_console import clear_console
from classes.AccountManager import AccountManager
from classes.Account import Account
from classes.UserChoiceManager import UserChoiceManager
from utils.misc import enter_to_continue
from utils.misc import clear_input_buffer
from termcolor import colored


def manage_students_screen(current_account: Account, choice_manager: UserChoiceManager) -> None:
    header = colored(f"<== Manage Students ==>", "cyan", attrs=["bold"])
    student_records = [] 
    controller = ManageStudentsController(current_account=current_account)

    def refresh_student_records():
        nonlocal student_records
        student_records = []

        controller.refresh_students()

        if len(controller.get_all_students()) == len(student_records):
            return
        
        for student_id, data in controller.get_all_students().items():
            student_records.append(
                {
                    # Format: id: number, student_id: string, data: dict { first_name: string, last_name: string, year_level: int, course: str }
                    "id": len(student_records) + 1,
                    "student_id": student_id,
                    "data": data
                }
            )


    refresh_student_records()

    while True:
        clear_console()
        line = "Record ID".ljust(12) + "Student ID".ljust(15) + "Name".ljust(25) + "Year Level".ljust(12) + "Course".ljust(20)

        prompt = colored(line, "white", attrs=["bold"])
        prompt += "\n" + ("-" * (12 + 15 + 25 + 12 + 20)) + "\n"

        refresh_student_records()

        #for student_record in student_records:

        choice_manager.set_prompt(new_prompt = prompt)
        choice_manager.set_options([
            "View Students",
            "Add Student",
            "Remove Student",
            "Back to Main Menu"
        ])

        choice = choice_manager.get_user_choice()
        match choice.label():
            case "Back to Main Menu":
                print("Returning to Main Menu...")
                enter_to_continue()
                return
            
            case "Add Student":
                # Determine next student ID from existing records.
                ids = [r.get("student_id") for r in student_records if r.get("student_id")]
                recent_id = ids[-1]
                prefix, suffix = recent_id.split("-")
                prefix = int(prefix) + 1 
                new_student_id = f"{str(prefix)}-{suffix}"

                first_name = input("Enter First Name: ").strip()
                last_name = input("Enter Last Name: ").strip()
                course = input("Enter Course: ").strip()
                phone_number = input("Enter Phone Number: ").strip()
                try:
                    year_level = int(input("Enter Year Level: "))
                except ValueError:
                    print("Year Level must be a number.")
                    enter_to_continue()
                    continue

                result = controller.create_student(student_id=new_student_id, first_name=first_name, last_name=last_name, year_level=year_level, course=course)
                if result.get("status"):
                    print(colored(f"Student '{first_name} {last_name}' added successfully (ID: {new_student_id}).", "green"))
                    # Refresh local records to include the new student
                    refresh_student_records()
                else:
                    print(colored(f"Failed to add student: {result.get('error')}", "red"))

                enter_to_continue()


            case other:
                print(f"You selected: {other}")
                enter_to_continue()

