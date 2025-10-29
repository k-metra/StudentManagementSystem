from classes.AccountManager import AccountManager
from classes.Account import Account 
from enums.permissions import Permissions
from roles import * # Import all roles
from dotenv import load_dotenv
import os
import json 

class ManageStudentsController:
    STUDENT_FILE = "src/data/students.json"
    def __init__(self, current_account: Account):
        self.account_manager = AccountManager()
        self.accounts = self.account_manager.load_accounts()
        self.current_account = current_account

        load_dotenv()

        self.DATA_FILE = os.getenv("students_DATA_FILE")

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
    def create_student(self, student_id: str, first_name: str, last_name: str, year_level: int, course: str) -> dict[str, str | bool]:
        if student_id in self.students:
            return {"status": False, "error" : "Student with that ID already exists."}
        
        self.students[student_id] = {
            "first_name": first_name,
            "last_name": last_name,
            "year_level": year_level,
            "course": course
        }
        self.save_students()
        return {"status": True, "message": f"Student '{student_id}' created successfully"}
    
