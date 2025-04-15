import sqlite3
import os


def configuring_database():
    # Create directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    # Configure SQLite connection
    db_path = 'data/database.db'
    db = sqlite3.connect(db_path)
    return db

def creating_database():
    db = configuring_database()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS password (id INTEGER PRIMARY KEY AUTOINCREMENT, password TEXT)")
    cursor.close()
    db.close()

# Storing password in database
def storing_password(password):
    db = configuring_database()
    # Creating table for storing password
    cursor = db.cursor()
    creating_database()
    cursor.execute("INSERT INTO password(password) VALUES(?)", (password,))
    db.commit()
    cursor.close()
    db.close()