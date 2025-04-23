"""
Script to handle database connection
"""

import sqlite3
import os


def configuring_database():
    """
    Configuring database connection to sqlite
    """
    # Create directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    # Configure SQLite connection
    db_path = "data/database.db"
    db = sqlite3.connect(db_path)
    return db


def creating_database():
    """
    Creating table if it does not exist to store passwords
    """
    # Configuring database
    db = configuring_database()
    # Creating table if it does not exist
    cursor = db.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS password (id INTEGER PRIMARY KEY AUTOINCREMENT, password TEXT)"
    )
    cursor.close()
    db.close()


def storing_password(password):
    """
    Inseting passwords into the tabse with auto incremented id
    """
    # Configuring database
    db = configuring_database()
    # Inserting passwords into table
    cursor = db.cursor()
    creating_database()
    cursor.execute("INSERT INTO password(password) VALUES(?)", (password,))
    db.commit()
    cursor.close()
    db.close()
