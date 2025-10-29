# Interactive Table System
## Overview
The interactive table system provides a comprehensive, reusable solutio nfor displaying tabular data in this console-based program with advanced features such as **pagination**, **filtering**, **searching**, and **item selection**.

The system is designed to be modular and easily integrated into any screen that needs to display data in table format.

The files are placed inside the `utils` package.

## Architecture
The system consists of two main components:
1. `TableDisplay` Class (`table_display.py`)
- **Purpose**: Core table rendering and data management
- **Responsibilities:**
    - Data storage and manipulation
    - Pagination logic
    - Filtering and searching
    - Table formatting and display generation

2. `interactive_table()` function (`table_interaction.py`)
- **Purpose:** User interaction and menu handling
- **Responsibilities:**
    - Menu option management
    - User input handling
    - Integration with `UserChoiceManager`
    - Callback execution for item selection

## Basic Usage
Simple table display

```py
from utils.table_interaction import interactive_table

# define data
data = [
    {"username": "admin", "role": "Administrator", "status": "Active"},
    {"username:" "user1", "role":"STudent","status":"Active"}
]

# Define column mapping (Data_field: display_header)
columns = {
    "username": "Username",
    "role": "Role",
    "status": "Status"
}

# Display the table
result = interactive_table(
    data=data,
    columns=columns,
    title="User Management",
)
```

### Advanced Usage with Item Selectoin
```py
def handle_user_select(selected_user: dict, item_id: int):
    print(f"Selected user: {selected_user['username']})
    # Handle the selected user...

result = interactive_table(
    data = data,
    columns=columns,
    title="User Management",
    additional_optoins=["Create New User, Import Users"],
    on_select_item=handle_user_select,
    items_per_page=5
)

if result == "Create New User":
    # Handle creating new user
    pass
elif result == "Import Users":
    # Handle importing users
    pass
```

## Function Parameters
Parameters for the `interactive_table()` function
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data` | `List[Dict[str, Any]]` | Yes | - | List of dictionaries containing the data to display |
| `columns` | `Dict[str, str]` | Yes | - | Mapping of data field names to display headers |
| `title` | `str` | Yes | - | Title displayed above the table |
| `additional_options` | `List[str]` | No | `[]` | Additional menu options to display |
| `on_select_item` | `Callable` | No | `None` | Callback function when item is selected |
| `items_per_page` | `int` | No | `10` | Number of items to display per page |

### Return Values
- `None`: User selected "Back" or exited
- `str`: Label of the selected additional option
- The function handles item selection internally via the callback

## (Potentially) Common Issues and Solutions
| Issue | Solution |
|-------|----------|
| Columns not displaying correctly | Ensure column keys in the `columns` dict match the keys in your data dictionaries exactly. |
| Pagination not working | Verify that your data is a list and contains more items than `items_per_page`. |
| Callback not being called | Ensure `on_select_item` parameter is passed and the function signature matches `(dict, int) -> None` |

# Example Implementation for Student Records Management
```py
def manage_students_screen():
    def get_students_data():
        # Fetch student data from database/file
        return [
            {"id": "S001", "name": "John Doe", "grade": "A", "gpa": "3.8"},
            {"id": "S002", "name": "Jane Smith", "grade": "B+", "gpa": "3.5"},
            # ... more students
        ]
    
    def handle_student_selection(selected_student: dict, item_id: int):
        # Handle student selection logic
        edit_student(selected_student["id"])
    
    columns = {
        "id": "Student ID",
        "name": "Full Name",
        "grade": "Current Grade",
        "gpa": "GPA"
    }
    
    while True:
        students_data = get_students_data()
        
        result = interactive_table(
            data=students_data,
            columns=columns,
            title="Student Records",
            additional_options=["Add New Student", "Import from CSV", "Generate Report"],
            on_select_item=handle_student_selection,
            items_per_page=15
        )
        
        if result is None:
            return
        elif result == "Add New Student":
            add_new_student()
        elif result == "Import from CSV":
            import_students_csv()
        elif result == "Generate Report":
            generate_student_report()
```