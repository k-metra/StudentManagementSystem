from classes.AccountManager import AccountManager
from classes.Account import Account 
from controllers.AuditLogController import AuditLogController
from enums.permissions import Permissions
from roles import * # Import all roles
from dotenv import load_dotenv
import os
import json

from utils.excel_import import import_students_from_excel 

class ManageStudentsController:
    def __init__(self, current_account: Account):
        self.account_manager = AccountManager()
        self.accounts = self.account_manager.load_accounts()
        self.current_account = current_account

        load_dotenv()

        self.DATA_FILE = os.getenv("STUDENTS_DATA_FILE", "src/data/students.json")
        self.STUDENT_FILE = self.DATA_FILE

    # utility Helpers

    def refresh_students(self):
        with open(self.STUDENT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.students = data.get("students", {})

    # Writes the current student data back to the JSON file
    def save_students(self):
        with open(self.STUDENT_FILE, "w", encoding="utf-8") as file:
            json.dump({"students": self.students}, file, indent=4)
    
    def get_all_students(self) -> dict[str, dict]:
        with open(self.STUDENT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.students = data.get("students", {})
        return self.students
    
    def create_student(self, student_id: str, first_name: str, last_name: str, year_level: int, phone_number: str, course: str, address: str, email: str, guardian_name: str, guardian_contact: str, dept: str) -> dict[str, str | bool]:
        if student_id in self.students:
            return {"status": False, "error" : "Student with that ID already exists."}
        
        self.students[student_id] = {
            "first_name": first_name,
            "last_name": last_name,
            "year_level": year_level,
            "phone_number": phone_number,
            "course": course,
            "home_address": address,
            "email_address": email,
            "guardian_name": guardian_name,
            "guardian_contact": guardian_contact,
            "department": dept

        }

        self.save_students()

        AuditLogController().add_log(
            action="Create",
            performed_by=self.current_account,
            application_name="Students",
            object_id=student_id,
            role=self.current_account.role
        )

        return {"status": True, "message": f"Student '{student_id}' created successfully"}
    
    def bulk_import_students(self, excel_path: str) -> dict[str, str | bool]:
        new_students = import_students_from_excel(excel_path)

        if not new_students:
            return {"status": False, "error": "No students were imported."}
        
        self.refresh_students()

        added, skipped = [], []

        for student_id, data in new_students.items():
            if student_id in self.students:
                skipped.append(student_id)
                continue
            
            self.students[student_id] = data
            added.append(student_id)

        self.save_students()
        AuditLogController().add_log(
            action="Bulk Import",
            performed_by=self.current_account,
            application_name="Students",
            object_id=", ".join(added),
            role=self.current_account.role
        )

        return {
            "status": True,
            "message": f"Bulk import completed. {len(added)} students added, {len(skipped)} (existing) students skipped."
        }

    
    def update_student(self, student_id: str, update_info: dict) -> dict[str, str | bool]:
        if student_id not in self.students:
            return {"status": False, "error": "Student with that ID does not exist."}

        self.students[student_id] = {**self.students[student_id], **update_info}
        self.save_students()

        AuditLogController().add_log(
            action="Update",
            performed_by=self.current_account,
            application_name="Students",
            object_id=student_id,
            role=self.current_account.role
        )

        return {"status": True, "message": f"Student '{student_id}' updated successfully."}

    def delete_student(self, student_id: str) -> dict[str, str | bool]:
        if student_id not in self.students:
            return {"status": False, "error": "Student with that ID does not exist."}
        
        del self.students[student_id]
        self.save_students()

        AuditLogController().add_log(
            action="Delete",
            performed_by=self.current_account,
            application_name="Students",
            object_id=student_id,
            role=self.current_account.role
        )

        return {"status": True, "message": f"Student '{student_id}' deleted successfully."}
    
    
