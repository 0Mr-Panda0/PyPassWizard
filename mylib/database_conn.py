import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def configuring_database():
    # Configure MySQL connection
    db = mysql.connector.connect(
        host=os.getenv('HOST_NAME'),
        port=int(os.getenv("PORT", 3333)),
        user=os.getenv('USER_NAME'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE_NAME')
    )
    return db

def creating_database():
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS password (id INT AUTO_INCREMENT PRIMARY KEY, password VARCHAR(255))")
    cursor.close()
    db.close()

# Storing password in database
def storing_password(password):
    db=configuring_database()
    # Creating table for storing password
    cursor = db.cursor()
    creating_database()
    cursor.execute("INSERT INTO password(password) VALUES(%s)", (password,))
    db.commit()
    cursor.close()