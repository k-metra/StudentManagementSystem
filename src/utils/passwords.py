import bcrypt

salt = bcrypt.gensalt(rounds=12)

def make_password(plain_text_password: str) -> str:
    """Hash a plain text password using bcrypt
    and return the hashed password as a string.

    Args:
        plain_text_password (str): The plain text password to hash.
    """

    global salt
    hashed = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')   

def check_password(plain_text_password: str, hashed_password: str) -> bool:
    """
        Check if a plain text password matches the hashed password.

        Args:
        plain_text_password (str): The plain text password to check.
        hashed_password (str): The hashed password to compare against.
    """

    global salt 

    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))