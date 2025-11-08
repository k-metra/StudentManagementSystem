from utils.passwords import make_password, check_password

def test_hash_and_check_password():
    plain_password = "pw"
    hashed_password = make_password(plain_password)

    assert hashed_password != plain_password

def test_check_password():
    password = "pw"
    hashed = make_password(password)

    assert check_password(password, hashed) is True
    assert check_password("wrong_pw", hashed) is False