from random import choice
from string import ascii_letters, digits, punctuation
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Configure MySQL connection
db = mysql.connector.connect(
    host=os.getenv('HOST_NAME'),
    port=int(os.getenv("PORT", 3333)),
    user=os.getenv('USER_NAME'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE_NAME')
)

def creating_table():
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS password (password VARCHAR(255))")
    cursor.close()


def storing_password(password):
    cursor = db.cursor()
    cursor.execute("INSERT INTO password(password) VALUES(%s)", (password,))
    db.commit()
    cursor.close()


def creating_password(length_of_password=11, if_special_character_allowed="Yes"):
    if if_special_character_allowed == "Yes":
        character = digits + ascii_letters + punctuation
    else:
        character = digits + ascii_letters
    return "".join(choice(character) for every_character in range(length_of_password))