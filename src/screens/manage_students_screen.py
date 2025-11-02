
from controllers import ManageStudentsController
from utils.clear_console import clear_console
from classes.AccountManager import AccountManager
from classes.Account import Account
from classes.UserChoiceManager import UserChoiceManager
from utils.table_interaction import interactive_table
from utils.misc import enter_to_continue
from utils.misc import clear_input_buffer
from termcolor import colored
from utils.acronym import acronymize, decronymize
import re

def edit_guardian_info(student_id: str, student: dict, controller: ManageStudentsController, header: list) -> dict | None:
    student_info = controller.get_all_students().get(student_id, {})
    clear_console() 

    print("\n".join(header))
    print(colored("== Edit Guardian Information ==\n", "white", attrs=["bold"]))
    print("Leave a field blank to keep the current value.\n")

    guardian_name = input(f"Guardian Name [{student.get('guardian_name', '')}]: ").strip()
    guardian_contact = input(f"Guardian Contact [{student.get('guardian_contact', '')}]: ").strip()

    student_info['guardian_name'] = guardian_name if guardian_name else student_info.get('guardian_name', '')
    student_info['guardian_contact'] = guardian_contact if guardian_contact else student_info.get('guardian_contact', '')

    print("\nConfirm information:")
    print(f"Guardian Name: {student_info['guardian_name']}")
    print(f"Guardian Contact: {student_info['guardian_contact']}\n")

    confirmation = input("Is the information correct? (y/n): ").strip().lower()

    if confirmation != 'y':
        print(colored("Update aborted.", "cyan"))
        enter_to_continue()
        return
    
    result = controller.update_student(student_id, student_info)
    if result.get("status"):
        print(colored(f"Guardian information updated successfully.", "green"))
        enter_to_continue()
        return student_info
    else:
        print(colored(f"Failed to update guardian information: {result.get('error')}", "red"))
        enter_to_continue()
        return

def edit_contact_info(student_id: str, student: dict, controller: ManageStudentsController, header: list) -> dict | None:
    student_info = controller.get_all_students().get(student_id, {})
    clear_console() 

    print("\n".join(header))
    print(colored("== Edit Contact Information ==\n", "white", attrs=["bold"]))
    print("Leave a field blank to keep the current value.\n")

    email_address = input(f"Email Address [{student.get('email_address', '')}]: ").strip()
    phone_number = input(f"Phone Number [{student.get('phone_number', '')}]: ").strip()
    home_address = input(f"Home Address [{student.get('home_address', '')}]: ").strip()

    student_info['email_address'] = email_address if email_address else student_info.get('email_address', '')
    student_info['phone_number'] = phone_number if phone_number else student_info.get('phone_number', '')
    student_info['home_address'] = home_address if home_address else student_info.get('home_address', '')

    print("\nConfirm information:")
    print(f"Email Address: {student_info['email_address']}")
    print(f"Phone Number: {student_info['phone_number']}")
    print(f"Home Address: {student_info['home_address']}\n")

    confirmation = input("Is the information correct? (y/n): ").strip().lower()

    if confirmation != 'y':
        print(colored("Update aborted.", "cyan"))
        enter_to_continue()
        return
    
    result = controller.update_student(student_id, student_info)
    if result.get("status"):
        print(colored(f"Contact information updated successfully.", "green"))
        enter_to_continue()
        return student_info
    else:
        print(colored(f"Failed to update contact information: {result.get('error')}", "red"))
        enter_to_continue()
        return

def edit_student_info(student_id: str, student: dict, controller: ManageStudentsController, header: list) -> dict | None:
    student_info = controller.get_all_students().get(student_id, {})
    clear_console()

    print("\n".join(header))
    print(colored("== Edit Student Information ==\n", "white", attrs=["bold"]))
    print("Leave a field blank to keep the current value.\n")
    first_name = input(f"First Name [{student.get('first_name', '')}]: ").strip()
    last_name = input(f"Last Name [{student.get('last_name', '')}]: ").strip()
    course = input(f"Course [{student.get('course', '')}]: ").strip()
    year_level_input = input(f"Year Level [{student.get('year_level', '')}]: ").strip()
    department = input(f"Department [{student.get('department', '')}]: ").strip()

    if first_name:
        student_info['first_name'] = first_name
    if last_name:
        student_info['last_name'] = last_name
    if course:
        student_info['course'] = course
    if year_level_input:
        student_info['year_level'] = year_level_input
    if department:
        student_info['department'] = department

    result = controller.update_student(student_id, student_info)

    if result.get("status"):
        print(colored(f"Student information updated successfully.", "green"))
        enter_to_continue()
        return student_info
    else:
        print(colored(f"Failed to update student information: {result.get('error')}", "red"))
        enter_to_continue()
        return

def manage_single_student(student: dict, controller: ManageStudentsController) -> None:
    choice_manager = UserChoiceManager()
    # student_name = student.get("full_name", "Unknown Student")
    student_id = student.get("student_id", "")

    while True:
        clear_console()

        # Refresh account data
        controller.refresh_students()
        all_students = controller.get_all_students()

        if student_id not in all_students:
            print(colored(f"Student with ID '{student_id}' no longer exists.", "red"))
            enter_to_continue()
            return
        
        student_data = all_students[student_id]
        student_name = student_data.get("last_name", "Unknown") + ", " + student_data.get("first_name", "Unknown")

        header = [
            colored(f"<== Managing Student: {student_id} ==>", "cyan", attrs=["bold"]),
            "",
            colored(f"== Student Information: ==", "white", attrs=["bold"]),
            colored(f"First Name:", "cyan", attrs=["bold"]) + colored(f" {student_data.get('first_name', 'Unknown')}", "white"),
            colored(f"Last Name:", "cyan", attrs=["bold"]) + colored(f" {student_data.get('last_name', 'Unknown')}", "white"),
            colored(f"Year Level:", "cyan", attrs=["bold"]) + colored(f" {student_data.get('year_level', 'Unknown')}", "white"),
            colored(f"Course:", "cyan", attrs=["bold"]) + colored(f" {student_data.get('course', 'Unknown')}", "white"),
            colored(f"Department:", "cyan", attrs=["bold"]) + colored(f" {decronymize(student_data.get('department', 'Unknown'))}", "white"),
            "",
            colored(f"== Contact Information: ==", "white", attrs=["bold"]),
            colored(f"Email Address:", "cyan", attrs=["bold"]) + colored(f" {student_data.get('email_address', 'Unknown')}", "white"),
            colored(f"Phone Number:", "cyan", attrs=["bold"]) + colored(f" {student_data.get('phone_number', 'Unknown')}", "white"),
            colored(f"Home Address:", "cyan", attrs=["bold"]) + colored(f" {student_data.get('home_address', 'Unknown')}", "white"),
            "",
            colored(f"== Guardian Information: ==", "white", attrs=["bold"]),
            colored(f"Guardian Name:", "cyan", attrs=["bold"]) + colored(f" {student_data.get('guardian_name', 'Unknown')}", "white"),
            colored(f"Guardian Contact:", "cyan", attrs=["bold"]) + colored(f" {student_data.get('guardian_contact', 'Unknown')}", "white"),
            "",
        ]
        
        choice_manager.set_prompt("\n".join(header))


        # In the future we'll instead build the options one-by-one based on permissions
        choice_manager.set_options([
            "Edit Student Information",
            "Edit Contact Information",
            "Edit Guardian Information",
            "Delete Student",
            "Back to Student List"
        ])

        choice = choice_manager.get_user_choice()

        match choice.label():
            case "Back to Student List":
                print("Returning back to Student List...")
                enter_to_continue()
                return
            case "Edit Student Information":
                # Handle editing student information
                updated_data = edit_student_info(student_id, student_data, controller, header)
                student = updated_data if updated_data else student_data
            case "Edit Contact Information":
                # Handle editing contact information
                updated_data = edit_contact_info(student_id, student_data, controller, header)
                student = updated_data if updated_data else student_data
            case "Edit Guardian Information":
                updated_data = edit_guardian_info(student_id, student_data, controller, header)
                student = updated_data if updated_data else student_data
            case "Delete Student":
                decision = input(colored(f"Are you sure you want to delete student '{student_name}' (ID: {student_id})? (y/n): ", "yellow")).strip().lower()
                if decision != 'y':
                    print(colored("Deletion aborted.", "cyan"))
                    enter_to_continue()
                    continue
                result = controller.delete_student(student_id=student_id)
                if result.get("status"):
                    print(colored(f"Student '{student_name}' (ID: {student_id}) deleted successfully.", "green"))
                    enter_to_continue()
                    return
                else:
                    print(colored(f"Failed to delete student: {result.get('error')}", "red"))
                    enter_to_continue()
                    continue



def manage_students_screen(current_account: Account, choice_manager: UserChoiceManager) -> None:
    header = colored(f"<== Manage Students ==>", "cyan", attrs=["bold"])
    controller = ManageStudentsController(current_account=current_account)

    def get_student_records():
        student_records = []

        controller.refresh_students()
        
        for student_id, data in controller.get_all_students().items():
            student_records.append(
                {
                    "id": len(student_records) + 1,
                    "student_id": student_id,
                    "full_name": f"{data.get('last_name', '')}, {data.get('first_name', '')}",
                    "phone_number": data.get("phone_number", ""),
                    "year_level": data.get("year_level", ""),
                    "course": data.get("course", ""),
                    "home_address": data.get("home_address", ""),
                    "email_address": data.get("email_address", ""),
                    "guardian_name": data.get("guardian_name", ""),
                    "guardian_contact": data.get("guardian_contact", ""),
                    "department": acronymize(data.get("department", "")) # Acronymize department name for compression
                }
            )
        
        return student_records

    def handle_student_select(selected_student: dict, item_id: int):
        # Handle student selection here
        manage_single_student(selected_student, controller)
        return


    while True:
        clear_console()
        student_records = get_student_records()

        columns = {
            "student_id": "Student ID",
            "full_name": "Full Name",
            "year_level": "Year Level",
            "course": "Course",
            "department": "Department"
        }

        result = interactive_table(
            data=student_records,
            columns=columns,
            title="Student Records",
            on_select_item=handle_student_select,
            additional_options=["Add Student"],
            items_per_page=10
        )

        match result:
            case "Add Student":
                ids = [r.get("student_id") for r in student_records if r.get("student_id")]
                student_id = ids[-1]
                prefix, suffix = student_id.split("-")
                prefix = int(prefix) + 1
                new_student_id = f"{str(prefix)}-{suffix}"

                # Handle adding a new student
                colored(f"<== Adding Student: {new_student_id} ==>", "cyan", attrs=["bold"]),
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                try:
                    year_level = int(input("(Input only the number of year. i.e First year = 1) Year Level: "))
                except ValueError:
                    print(colored("Invalid input for year level. You must choose between year 1-4. Student creation aborted.", "red"))
                    enter_to_continue()
                    continue
                course = input("Course: ")
                address = input("Home Address: ")
                email = input("Email Address: ")
                phone_number = input("Phone Number: ")
                guardian_name = input("Guardian Name: ")
                guardian_contact = input("Guardian Contact: ")
                dept = input("Department: ")

                colored(f"\n\n<== Confirm Student Information ==>", "cyan", attrs=["bold"]),
                print(f"First name: {first_name}")
                print(f"Last name: {last_name}")
                print(f"Year Level: {year_level}")
                print(f"Course: {course}")
                print(f"Home Address: {address}")
                print(f"Email Address: {email}")
                print(f"Phone Number: {phone_number}")
                print(f"Guardian Name: {guardian_name}")
                print(f"Guardian Contact: {guardian_contact}")
                decision = input(colored("Is the information correct? (y/n): ", "yellow")).strip().lower()
                if decision != 'y':
                    print("Student Creation is aborted.")
                else:
                    controller.create_student(
                        student_id=new_student_id,
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        year_level=year_level,
                        course=course,
                        address=address,
                        email=email,
                        guardian_name = guardian_name,
                        guardian_contact = guardian_contact,
                        dept = dept
                    )
                    
                    
            case None:
                return
            case other:
               continue


        #for student_record in student_records:

        # choice_manager.set_prompt(new_prompt = prompt)
        # choice_manager.set_options([
        #     "View Students",
        #     "Add Student",
        #     "Update Student",
        #     "Remove Student",
        #     "Back to Main Menu"
        # ])


