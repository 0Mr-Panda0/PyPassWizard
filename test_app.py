from mylib.password_generator import creating_password
from mylib.database_conn import configuring_database, storing_password
from string import punctuation


# test database connection
def test_database_connection():
    db = configuring_database()
    assert db is not None, "Database connection established"
    db.close()


def test_creating_password():
    # Test case 1: If special character is allowed
    case_1 = creating_password(10, "Yes")
    assert len(case_1) == 10
    assert any(character in case_1 for character in punctuation)
    # Test case 2: If special character is not allowed
    case_2 = creating_password(10, "No")
    assert len(case_2) == 10
    assert all(character.isalnum() for character in case_2)


def test_storing_password():
    case_1 = creating_password(13, "Yes")
    storing_password(case_1)
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM password WHERE password=?", (case_1,))
    assert cursor.fetchone()[1] == case_1, "Password stored in database"
    cursor.close()


def test_creating_password_length():
    # Test case: Check if the password length is as expected
    length = 15
    password = creating_password(length, "Yes")
    assert len(password) == length, "Password length should be 15"


def test_creating_password_no_special_characters():
    # Test case: Check if the password contains no special characters when not allowed
    password = creating_password(12, "No")
    assert all(
        character.isalnum() for character in password
    ), "Password should not contain special characters"


def test_creating_password_with_special_characters():
    # Test case: Check if the password contains at least one special character when allowed
    password = creating_password(12, "Yes")
    assert any(
        character in password for character in punctuation
    ), "Password should contain special characters"


def test_storing_password_not_stored():
    # Test case: Check if the password is not stored when storing is not allowed
    case_1 = creating_password(13, "Yes")
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM password WHERE password=?", (case_1,))
    assert cursor.fetchone() is None, "Password should not be stored in database"
    cursor.close()
