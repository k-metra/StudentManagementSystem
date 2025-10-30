def acronymize(phrase: str) -> str:
    """Generate an acronym from a given phrase.
    Good for college departments, e.g. CCS -> College of Computer Studies
    """

    non_acronym_words = ["of", "and", "the", "for", "in", "on", "at"]

    words = phrase.split()
    acronym = "".join(word[0].upper() for word in words if word not in non_acronym_words)

    return acronym 

def decronymize(acronym: str, mapping: dict | None = None) -> str:

    mapping = mapping or {
        "CCS":      "College of Computer Studies",
        "CAS":      "College of Arts and Sciences",
        "COENG":    "College of Engineering",
        "CBM":      "College of Business Management",
        "COL":      "College of Law",
        "CCJ":      "College of Criminal Justice",
        "CTHM":     "College of Tourism and Hospitality Management",
        "COED":     "College of Education",
        "CAS":      "College of Arts and Sciences",

        # Courses
        "BSIT":     "Bachelor of Science in Information Technology",
        "BSCS":     "Bachelor of Science in Computer Science",
        "BSBA":     "Bachelor of Science in Business Administration",
        "BSE":      "Bachelor of Science in Education",
        "BSTM":     "Bachelor of Science in Tourism Management",
        "BSCE":     "Bachelor of Science in Civil Engineering",
        "BSCrim":   "Bachelor of Science in Criminology",
        "LLB":      "Bachelor of Laws",
        "MD":       "Doctor of Medicine",
        "DICT":     "Diploma in Computer Technology",
    }

    return mapping.get(acronym.upper(), acronym)