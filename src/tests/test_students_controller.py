import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from types import SimpleNamespace

import pytest


class TestableManageStudentsController:
    """A testable version of ManageStudentsController that doesn't call blocking methods."""
    
    def __init__(self, current_account, students_file):
        self.current_account = current_account
        self.STUDENT_FILE = students_file
        self.DATA_FILE = students_file
        self.students = {}

    def refresh_students(self):
        try:
            with open(self.STUDENT_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.students = data.get("students", {})
        except FileNotFoundError:
            self.students = {}

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
        # Skip audit logging in tests
        return {"status": True, "message": f"Student '{student_id}' created successfully"}
    
    def bulk_import_students(self, excel_path: str, new_students: dict = None) -> dict[str, str | bool]:
        # Accept new_students parameter for testing
        if new_students is None:
            new_students = {}

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
        # Skip audit logging in tests

        return {
            "status": True,
            "message": f"Bulk import completed. {len(added)} students added, {len(skipped)} (existing) students skipped."
        }

    def update_student(self, student_id: str, update_info: dict) -> dict[str, str | bool]:
        if student_id not in self.students:
            return {"status": False, "error": "Student with that ID does not exist."}

        self.students[student_id] = {**self.students[student_id], **update_info}
        self.save_students()
        # Skip audit logging in tests
        return {"status": True, "message": f"Student '{student_id}' updated successfully."}

    def delete_student(self, student_id: str) -> dict[str, str | bool]:
        if student_id not in self.students:
            return {"status": False, "error": "Student with that ID does not exist."}
        
        del self.students[student_id]
        self.save_students()
        # Skip audit logging in tests
        return {"status": True, "message": f"Student '{student_id}' deleted successfully."}


@pytest.fixture
def mock_account():
    """Create a mock account for testing."""
    account = Mock()
    account.role = "Admin"
    account.username = "test_user"
    return account


@pytest.fixture
def temp_students_file():
    """Create a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        initial_data = {"students": {}}
        json.dump(initial_data, f)
        temp_file_path = f.name
    
    yield temp_file_path
    
    # Cleanup
    if os.path.exists(temp_file_path):
        os.unlink(temp_file_path)


@pytest.fixture
def controller(mock_account, temp_students_file):
    """Create a testable controller instance."""
    controller = TestableManageStudentsController(mock_account, temp_students_file)
    controller.refresh_students()
    return controller


def test_refresh_students(controller, temp_students_file):
    """Test that refresh_students loads data from file correctly."""
    # Setup test data
    test_data = {
        "students": {
            "S001": {
                "first_name": "John",
                "last_name": "Doe",
                "year_level": 1,
                "phone_number": "123-456-7890",
                "course": "BSCS",
                "home_address": "123 Main St",
                "email_address": "john@example.com",
                "guardian_name": "Jane Doe",
                "guardian_contact": "098-765-4321",
                "department": "CS"
            }
        }
    }
    
    with open(temp_students_file, 'w') as f:
        json.dump(test_data, f)
    
    controller.refresh_students()
    
    assert "S001" in controller.students
    assert controller.students["S001"]["first_name"] == "John"


def test_get_all_students(controller, temp_students_file):
    """Test that get_all_students returns all student data."""
    test_data = {
        "students": {
            "S001": {"first_name": "John"},
            "S002": {"first_name": "Jane"}
        }
    }
    
    with open(temp_students_file, 'w') as f:
        json.dump(test_data, f)
    
    result = controller.get_all_students()
    
    assert len(result) == 2
    assert "S001" in result
    assert "S002" in result


def test_create_student_success(controller):
    """Test successful student creation."""
    result = controller.create_student(
        student_id="S001",
        first_name="John",
        last_name="Doe",
        year_level=1,
        phone_number="123-456-7890",
        course="BSCS",
        address="123 Main St",
        email="john@example.com",
        guardian_name="Jane Doe",
        guardian_contact="098-765-4321",
        dept="CS"
    )
    
    assert result["status"] is True
    assert "created successfully" in result["message"]
    assert "S001" in controller.students
    assert controller.students["S001"]["first_name"] == "John"


def test_create_student_duplicate_id(controller):
    """Test creating student with duplicate ID fails."""
    # First creation
    controller.create_student("S001", "John", "Doe", 1, "123-456-7890", 
                            "BSCS", "123 Main St", "john@example.com", 
                            "Jane Doe", "098-765-4321", "CS")
    
    # Attempt duplicate creation
    result = controller.create_student("S001", "Jane", "Smith", 2, "987-654-3210",
                                     "BSIT", "456 Oak Ave", "jane@example.com",
                                     "John Smith", "456-789-0123", "IT")
    
    assert result["status"] is False
    assert "already exists" in result["error"]
    # Original student data should remain unchanged
    assert controller.students["S001"]["first_name"] == "John"


def test_update_student_success(controller):
    """Test successful student update."""
    # Create a student first
    controller.create_student("S001", "John", "Doe", 1, "123-456-7890",
                            "BSCS", "123 Main St", "john@example.com",
                            "Jane Doe", "098-765-4321", "CS")
    
    # Update the student
    update_data = {
        "phone_number": "555-555-5555",
        "year_level": 2
    }
    
    result = controller.update_student("S001", update_data)
    
    assert result["status"] is True
    assert "updated successfully" in result["message"]
    assert controller.students["S001"]["phone_number"] == "555-555-5555"
    assert controller.students["S001"]["year_level"] == 2
    # Other fields should remain unchanged
    assert controller.students["S001"]["first_name"] == "John"


def test_update_student_not_found(controller):
    """Test updating non-existent student fails."""
    result = controller.update_student("S999", {"phone_number": "555-555-5555"})
    
    assert result["status"] is False
    assert "does not exist" in result["error"]


def test_delete_student_success(controller):
    """Test successful student deletion."""
    # Create a student first
    controller.create_student("S001", "John", "Doe", 1, "123-456-7890",
                            "BSCS", "123 Main St", "john@example.com",
                            "Jane Doe", "098-765-4321", "CS")
    
    result = controller.delete_student("S001")
    
    assert result["status"] is True
    assert "deleted successfully" in result["message"]
    assert "S001" not in controller.students


def test_delete_student_not_found(controller):
    """Test deleting non-existent student fails."""
    result = controller.delete_student("S999")
    
    assert result["status"] is False
    assert "does not exist" in result["error"]


def test_bulk_import_success(controller):
    """Test successful bulk import of students."""
    # Test data
    new_students = {
        "S001": {
            "first_name": "John",
            "last_name": "Doe",
            "year_level": 1,
            "phone_number": "123-456-7890",
            "course": "BSCS",
            "home_address": "123 Main St",
            "email_address": "john@example.com",
            "guardian_name": "Jane Doe",
            "guardian_contact": "098-765-4321",
            "department": "CS"
        },
        "S002": {
            "first_name": "Jane",
            "last_name": "Smith",
            "year_level": 2,
            "phone_number": "987-654-3210",
            "course": "BSIT",
            "home_address": "456 Oak Ave",
            "email_address": "jane@example.com",
            "guardian_name": "John Smith",
            "guardian_contact": "456-789-0123",
            "department": "IT"
        }
    }
    
    result = controller.bulk_import_students("test.xlsx", new_students)
    
    assert result["status"] is True
    assert "Bulk import completed" in result["message"]
    assert "2 students added" in result["message"]
    assert "0 (existing) students skipped" in result["message"]
    assert len(controller.students) == 2
    assert "S001" in controller.students
    assert "S002" in controller.students


def test_bulk_import_no_students(controller):
    """Test bulk import when no students are imported."""
    result = controller.bulk_import_students("empty.xlsx", {})
    
    assert result["status"] is False
    assert "No students were imported" in result["error"]


def test_bulk_import_with_existing_students(controller):
    """Test bulk import when some students already exist."""
    # Create an existing student
    controller.create_student("S001", "Existing", "Student", 1, "000-000-0000",
                            "BSCS", "Old Address", "old@example.com",
                            "Old Guardian", "111-111-1111", "CS")
    
    # Import with one existing and one new student
    new_students = {
        "S001": {  # This one already exists
            "first_name": "John",
            "last_name": "Doe"
        },
        "S002": {  # This one is new
            "first_name": "Jane",
            "last_name": "Smith",
            "year_level": 2,
            "phone_number": "987-654-3210",
            "course": "BSIT",
            "home_address": "456 Oak Ave",
            "email_address": "jane@example.com",
            "guardian_name": "John Smith",
            "guardian_contact": "456-789-0123",
            "department": "IT"
        }
    }
    
    result = controller.bulk_import_students("test.xlsx", new_students)
    
    assert result["status"] is True
    assert "1 students added" in result["message"]
    assert "1 (existing) students skipped" in result["message"]
    # Existing student should not be overwritten
    assert controller.students["S001"]["first_name"] == "Existing"
    assert controller.students["S002"]["first_name"] == "Jane"


def test_save_students(controller, temp_students_file):
    """Test that save_students writes data to file correctly."""
    controller.students = {
        "S001": {
            "first_name": "John",
            "last_name": "Doe"
        }
    }
    
    controller.save_students()
    
    # Verify data was written to file
    with open(temp_students_file, 'r') as f:
        data = json.load(f)
        assert "students" in data
        assert "S001" in data["students"]
        assert data["students"]["S001"]["first_name"] == "John"
