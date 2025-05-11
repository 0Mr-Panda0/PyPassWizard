"""
This module provides a database class for handling password storage and retrieval.
"""

import sqlite3
import os
import logging
import pandas as pd  # type: ignore
from pandera.typing import DataFrame


class Database:
    """
    Database class for managing password storage and retrieval.
    """

    def __init__(self, path: str) -> None:
        self.db_path: str = os.path.abspath(path)
        self.create_database_path()
        self.creating_table()

    def create_database_path(self) -> None:
        data_dir = os.path.dirname(self.db_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logging.info(f"Created directory: {data_dir}")

    def creating_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS password (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            password TEXT
        )
        """
        self.execute_query(query)

    def execute_query(self, query: str, params: tuple = ()) -> list:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                result = cursor.fetchall()
                conn.commit()
                return result
        except sqlite3.Error as e:
            logging.error(f"Database query failed: {e}")
            raise ConnectionError(f"{e}")

    def inserting_password(self, name: str, password: str) -> None:
        if not password:
            raise ValueError("Password cannot be empty.")
        self.execute_query(
            "INSERT INTO password(name, password) VALUES(?, ?)", (name, password)
        )
        logging.info(f"Password for name '{name}' inserted successfully.")

    def retrieve_password_with_name(self, name: str) -> str:
        result = self.execute_query(
            "SELECT password FROM password WHERE name = ?", (name,)
        )
        if result:
            return result[0][0]
        raise ValueError(f"No password associated with name: {name}")

    def delete_password_with_name(self, name: str) -> None:
        self.execute_query("DELETE FROM password WHERE name = ?", (name,))
        logging.info(f"Password for name '{name}' deleted successfully.")

    def show_all_passwords(self) -> DataFrame:
        result = self.execute_query("SELECT name, password FROM password")
        df = pd.DataFrame(result, columns=["name", "password"])
        if not df.empty:
            return df
        raise ValueError("No data found in the 'password' table.")

    def bulk_insert_passwords(self, data: DataFrame) -> None:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame.")
        if data.empty:
            raise ValueError("DataFrame is empty.")
        if not all(col in data.columns for col in ["name", "password"]):
            raise ValueError("DataFrame must contain 'name' and 'password' columns.")

        data = data.drop_duplicates(subset=["name"])
        data.to_sql(
            "password", sqlite3.connect(self.db_path), if_exists="append", index=False
        )
        logging.info("Bulk insert of passwords completed successfully.")
