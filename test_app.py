from mylib.password_generator import creating_password
from mylib.database_conn import configuring_database, storing_password
from string import punctuation
import mysql.connector
import os


def test_database_connection():
    db = configuring_database()
    assert db.is_connected(), "Database connected successfully"


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
    cursor.execute("SELECT * FROM password WHERE password=%s", (case_1,))
    assert cursor.fetchone()[1] == case_1, "Password stored in database"
    cursor.close()
