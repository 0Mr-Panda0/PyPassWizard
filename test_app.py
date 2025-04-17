from mylib.password_generator import creating_password
from mylib.database_conn import (
    configuring_database,
    storing_password,
)
from string import punctuation
import random


def test_database_connection():
    # Test case: database connection
    db = configuring_database()
    assert db is not None, "Database connection established"
    db.close()


def test_storing_password():
    # Test case: Check if the password is stored in the database
    case_1 = creating_password(random.randint(8, 20), True)
    storing_password(case_1)
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM password WHERE password=?", (case_1,))
    assert cursor.fetchone()[1] == case_1, "Password stored in database"
    cursor.execute("DELETE FROM password WHERE password=?", (case_1,))
    db.commit()
    cursor.close()


def test_creating_password_length():
    # Test case: Check if the password length is as expected
    length = random.randint(8, 20)
    password = creating_password(length, True)
    assert len(password) == length, f"Password length should be {length}"


def test_creating_password_no_special_characters():
    # Test case: Check if the password contains no special characters when not allowed
    password = creating_password(random.randint(8, 20), False)
    assert all(
        character.isalnum() for character in password
    ), "Password should not contain special characters"


def test_creating_password_with_special_characters():
    # Test case: Check if the password contains at least one special character when allowed
    password = creating_password(random.randint(8, 20), True)
    assert any(
        character in password for character in punctuation
    ), "Password should contain special characters"


def test_storing_password_not_stored():
    # Test case: Check if the password is not stored when storing is not allowed
    case_1 = creating_password(random.randint(8, 20), True)
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM password WHERE password=?", (case_1,))
    assert cursor.fetchone() is None, "Password should not be stored in database"
    cursor.close()
