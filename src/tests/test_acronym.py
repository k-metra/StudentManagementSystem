from utils.acronym import acronymize, decronymize

def test_acronymize():
    phrase = "As soon as possible"
    expected_acronym = "ASAP"

    assert acronymize(phrase) == expected_acronym

def test_decronymize():
    acronym = "CCS"

    assert decronymize(acronym) == "College of Computer Studies"

def test_ccs_acronym():
    assert acronymize("College of Computer Studies") == "CCS"

def test_course_acronym():
    courses = [
        "Bachelor of Science in Computer Science",
        "Bachelor of Science in Information Technology",
        "Bachelor of Science in Business Administration",
        "Bachelor of Science in Hospitality Management",   
    ]

    acronyms = [True if acronymize(course) == expected else False for course, expected in zip(courses, ["BSCS", "BSIT", "BSBA", "BSHM"])]

    assert all(acronyms) is True

def test_department_acronyms():
    departments = {
        "College of Computer Studies": "CCS",
        "College of Criminal Justice": "CCJ",
        "College of Tourism and Hospitality Management": "CTHM",
    }

    acronyms = [True if acronymize(dept_name) else False for dept_name, expected in departments.items()]

    assert all(acronyms) is True