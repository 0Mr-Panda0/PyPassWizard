"""
Test cases for the Database class in the utility module.
"""

import os
import sqlite3
import pytest
import funkybob  # type: ignore
from src.utility import Database
from src.core import PasswordGenerator
from dotenv import load_dotenv

load_dotenv()


class TestDatabase:
    """
    Test cases for the Database class.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Setup and teardown for the test cases.
        This fixture creates a new database instance before each test and
        removes the database file after each test.
        """
        # Setup
        self.db_instance = Database(str(os.getenv("TEST_DB_PATH", "data/test.db")))
        yield
        # Teardown
        if os.path.exists(self.db_instance.db_path):
            os.remove(self.db_instance.db_path)

    @pytest.fixture
    def pass_gen(self) -> PasswordGenerator:
        """
        Fixture for the password generation.

        Returns:
            PasswordGenerator: PasswordGenerator class.
        """
        return PasswordGenerator()

    @pytest.fixture
    def name_gen(self) -> funkybob:
        """
        Fixture for the password generation.

        Returns:
            PasswordGenerator: PasswordGenerator class.
        """
        return funkybob.RandomNameGenerator()

    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        Execute a query on the test database.

        Args:
            query (str): The SQL query to execute.
            params (tuple): Parameters for the query.

        Returns:
            list: Query results.
        """
        with sqlite3.connect(self.db_instance.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def test_database_path_creation(self) -> None:
        """
        Test if the database path is created correctly.
        """
        data_dir = os.path.dirname(self.db_instance.db_path)
        assert os.path.exists(data_dir), "Database directory should exist."

    def test_table_creation(self) -> None:
        """
        Test if the password table is created in the database.
        """
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{str(os.getenv('TEST_TABLE_NAME', 'password'))}';"
        result = self.execute_query(query)
        assert result, (
            f"Table '{str(os.getenv('TEST_TABLE_NAME', 'password'))}' should exist."
        )

    def test_insert_password(
        self, pass_gen: PasswordGenerator, name_gen: funkybob.RandomNameGenerator
    ) -> None:
        """
        Test if a password can be inserted into the database.
        """
        test_password = pass_gen.generate_password(12, True, True, True)
        test_name = next(iter(name_gen))

        self.db_instance.inserting_password(test_name, test_password)
        result = self.execute_query(
            f"SELECT password FROM {str(os.getenv('TEST_TABLE_NAME', 'password'))} WHERE name = ?",
            (test_name,),
        )
        self.db_instance.delete_password_with_name(test_name)

        assert result, "Password should be inserted into the database."
        assert result[0][0] == test_password, (
            "Inserted password should match the test password."
        )

    def test_retrieve_non_existent_password(self) -> None:
        """
        Test if retrieving a non-existent password raises a ValueError.
        """
        with pytest.raises(ValueError, match="No password associated with name:"):
            self.db_instance.retrieve_password_with_name("non_existent_name")

    def test_delete_password(
        self, pass_gen: PasswordGenerator, name_gen: funkybob.RandomNameGenerator
    ) -> None:
        """
        Test if a password can be deleted from the database.
        """
        test_password = pass_gen.generate_password(12, True, True, True)
        test_name = next(iter(name_gen))

        self.db_instance.inserting_password(test_name, test_password)
        self.db_instance.delete_password_with_name(test_name)

        with pytest.raises(ValueError, match="No password associated with name:"):
            self.db_instance.retrieve_password_with_name(test_name)
