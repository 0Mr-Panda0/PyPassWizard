from dotenv import load_dotenv
import sqlite3
import os

# Load environment variables from .env file
load_dotenv()


def configuring_database():
    # Configure SQLite connection
    db_path = os.getenv("DB_PATH")
    db = sqlite3.connect(db_path)
    return db


print(configuring_database())
