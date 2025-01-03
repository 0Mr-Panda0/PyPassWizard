from mylib.password_generator import creating_password, storing_password
from string import punctuation
import mysql.connector
import os


def test_database_connection():
    db = mysql.connector.connect(
        host=os.getenv("HOST_NAME"),
        port=os.getenv("PORT"),
        user=os.getenv("USER_NAME"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE_NAME"),
    )
    assert db.is_connected() == True


def test_creating_password():
    case_1 = creating_password(10, "Yes")
    assert len(case_1) == 10
    assert any(character in case_1 for character in punctuation)
    case_2 = creating_password(10, "No")
    assert len(case_2) == 10
    assert all(character.isalnum() for character in case_2)


def test_storing_password():
    case_1 = creating_password(13, "Yes")
    storing_password(case_1)
    db = mysql.connector.connect(
        host=os.getenv("HOST_NAME"),
        port=os.getenv("PORT"),
        user=os.getenv("USER_NAME"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE_NAME"),
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM password WHERE password=%s", (case_1,))
    assert cursor.fetchone()[1] == case_1, "Password stored in database"
    cursor.close()
