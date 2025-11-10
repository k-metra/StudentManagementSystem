import re


def validate_phone(num) -> bool:
    pattern = r"^(\+63|0)?[\s-]?(\d{3})[\s-]?(\d{3})[\s-]?(\d{4})$"

    return bool(re.match(pattern, num))

def format_phone(num) -> str:

    num = re.sub(r"\D", "", num)

    if num.startswith("0"):
        num = "+63" + num[1:]
    elif not num.startswith("+63"):
        num = "+63" + num

    pattern = r"^(?:\+63)(\d{3})(\d{3})(\d{4})$"
    match = re.match(pattern, num)
    if match:
        print("Matched, returning " + f"+63 {match.group(1)} {match.group(2)} {match.group(3)}")
        return f"+63 {match.group(1)} {match.group(2)} {match.group(3)}"
    
    print("Didn't match")
    return num