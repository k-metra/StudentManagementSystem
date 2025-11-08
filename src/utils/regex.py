import re


def validate_phone(num) -> bool:
    pattern = r"^(\+63|0)?[\s-]?(\d{3})[\s-]?(\d{3})[\s-]?(\d{4})$"

    return bool(re.match(pattern, num))

def format_phone(num) -> str:
    pattern = r"^(?:\+63)(\d{3})(\d{3})(\d{4})$"
    match = re.match(pattern, num)
    if match:
        return f"+63 {match.group(1)} {match.group(2)} {match.group(3)}"
    
    return num