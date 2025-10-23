from classes.AccountManager import AccountManager
from classes.Account import Account 
from enums.permissions import Permissions
from roles import * # Import all roles
from typing import Tuple
import json 

class ManageStudentsController:
   from classes.Account import Account
from enums.permissions import Permissions
from typing import Dict, Any, Optional
import json

class ManageStudentController:
   class ManageStudentController:
    # Changed to a students data file
    DATA_FILE = "src/data/students.json"

    def __init__(self, current_account: Account):
        self.current_account = current_account
        self.students = self._load_students()

    # ---------------
    # Utility Helpers
    # ---------------

    def _load_students(self) -> Dict[str, Dict[str, Any]]:
        """Loads all student records from the JSON file."""
        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("students", {})
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {self.DATA_FILE}. Returning empty student list.")
            return {}

    def save_students(self):
         # Writes the current student records back to the JSON file.
        with open(self.DATA_FILE, "w", encoding="utf-8") as file:
            # Write the data in the required format: {"students": {...}}
            json.dump({"students": self.students}, file, indent=4)

    # ---------------
    # CRUD Operations
    # ---------------

    def get_all_students(self) -> Dict[str, Dict[str, Any]]:
        """Returns all student records."""
        return self.students

    def add_record(self, student_id: str, first_name: str, last_name: str, phone_number: str, year_level: int, course: str) -> Dict[str, str | bool]:
        """Adds a new student record using the fields from the sample data."""
        if not self.current_account.has_permission(Permissions.ADD_RECORD):
            return {"status": False, "error": "You don't have permission to add student records."}

        if student_id in self.students:
            return {"status": False, "error": f"Student with ID '{student_id}' already exists."}
        
        # Basic data validation (you may want to add more robust checks)
        if not (first_name and last_name and student_id and isinstance(year_level, int)):
             return {"status": False, "error": "Invalid data provided (e.g., missing name or year level not an integer)."}

        self.students[student_id] = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "year_level": year_level,
            "course": course
        }

        self.save_students()
        return {"status": True, "message": f"Student record for ID '{student_id}' created successfully."}

    def edit_record(self, student_id: str, first_name: Optional[str] = None, last_name: Optional[str] = None, phone_number: Optional[str] = None, year_level: Optional[int] = None, course: Optional[str] = None) -> Dict[str, str | bool]:
        """Edits an existing student record. Only updates provided fields."""
        if not self.current_account.has_permission(Permissions.EDIT_RECORD):
            return {"status": False, "error": "You don't have permission to edit student records."}

        if student_id not in self.students:
            return {"status": False, "error": f"No student with ID '{student_id}' exists."}
        
        updated = False
        record = self.students[student_id]

        if first_name is not None:
            record["first_name"] = first_name
            updated = True
        
        if last_name is not None:
            record["last_name"] = last_name
            updated = True
            
        if phone_number is not None:
            record["phone_number"] = phone_number
            updated = True
            
        if year_level is not None:
            if not isinstance(year_level, int):
                return {"status": False, "error": "Year level must be an integer."}
            record["year_level"] = year_level
            updated = True
        
        if course is not None:
            record["course"] = course
            updated = True

        if updated:
            self.save_students()
            return {"status": True, "message": f"Student record for ID '{student_id}' updated successfully."}
        else:
            return {"status": False, "error": f"No valid changes were provided for student ID '{student_id}'."}


    def delete_record(self, student_id: str) -> Dict[str, str | bool]:
        """Deletes a student record based on their ID."""
        if not self.current_account.has_permission(Permissions.DELETE_RECORD):
            return {"status": False, "error": "You don't have permission to delete student records."}

        if student_id not in self.students:
            return {"status": False, "error": f"No student with ID '{student_id}' exists."}
        
        del self.students[student_id]
        self.save_students()
        return {"status": True, "message": f"Student record for ID '{student_id}' deleted successfully."}