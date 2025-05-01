"""
This module provides a database class for handling password storage and retrieval.
"""

import sqlite3
import os
import logging


class Database:
    """
    Database class for managing password storage and retrieval.
    """

    def __init__(self, path: str):
        """
        Initializes the Database class, sets up the database path.

        Args:
            path (str): path to the database.
        """
        self.db_path = os.path.abspath(path)
        self.db = self.configuring_database()
        self.creating_table()

    def create_database_path(self) -> None:
        """
        Creates the directory for the database if it does not exist.
        """
        data_dir = os.path.dirname(self.db_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logging.info(f"Created directory: {data_dir}")

    def configuring_database(self) -> sqlite3.Connection:
        """
        Configures the database connection.

        Returns:
            sqlite3.Connection: Database connection object.
        """
        self.create_database_path()
        try:
            db = sqlite3.connect(self.db_path)
            logging.info(f"Connected to database at {self.db_path}")
            return db
        except sqlite3.Error as e:
            logging.error(f"Failed to connect to database: {e}")
            raise

    def creating_table(self) -> None:
        """
        Creates the password table if it does not exist.
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS password (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT)"
            )
            self.db.commit()
            cursor.close()
            logging.info("Table 'password' ensured to exist.")
        except sqlite3.Error as e:
            logging.error(f"Failed to create table: {e}")
            raise

    def inserting_password(self, name: str, password: str) -> None:
        """
        Inserts a password into the database.
        Args:
            password (str): The password to be inserted.

        Raises:
            ValueError: If the password is empty.
        """
        if not password:
            logging.error("Password cannot be empty.")
            raise ValueError("Password cannot be empty.")
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO password(name,password) VALUES(?,?)", (name, password)
            )
            self.db.commit()
            cursor.close()
            logging.info("Password inserted successfully.")
        except sqlite3.Error as e:
            logging.error(f"Failed to insert password: {e}")
            raise

    def retrieve_password_with_name(self, name: str) -> str | None:
        """
        Retrieves password with provided name

        Args:
            name (str): Name associated with a password

        Returns:
            str: password associated with the name
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(f"SELECT password FROM password WHERE name = '{name}'")
            result = cursor.fetchone()
            cursor.close()
            if result:
                logging.info("Password retrieved successfully.")
                return result[0]
            else:
                logging.warning("No passwords found in the database.")
                return None
        except sqlite3.Error as e:
            logging.error(f"Failed to retrieve password: {e}")
            return None

    def delete_password_with_name(self, name: str) -> None:
        """
        Deleting the password associated withe the name

        Args:
            name (str): name for which the associated password must be deleted.
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(f"DELETE FROM password WHERE name = '{name}'")
            self.db.commit()
            cursor.close()
            logging.info(f"Password associated with name: {name} has been deleted!")
        except sqlite3.Error as e:
            logging.error(f"Failed to insert password: {e}")
            raise

    def close_connection(self) -> None:
        """
        Closes the database connection.
        """
        if self.db:
            self.db.close()
            logging.info("Database connection closed.")
