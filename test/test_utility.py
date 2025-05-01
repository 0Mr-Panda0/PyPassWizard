"""
Test cases for the Database class in the utility module.
"""

import os
import sqlite3
import pytest
import funkybob  # type: ignore
from src.utility import Database
from src.core import PasswordGenerator
import random


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
        self.db_instance = Database("data/test.db")
        yield
        self.db_instance.close_connection()
        if os.path.exists(self.db_instance.db_path):
            os.remove(self.db_instance.db_path)

    @pytest.fixture
    def name_gen(self) -> funkybob:
        """
        Fixture for the Name generation.

        Returns:
            funkybob: An instance of funkybob
        """

        return funkybob.RandomNameGenerator()

    @pytest.fixture
    def pass_gen(self) -> PasswordGenerator:
        """
        Fixture for the password generation

        Returns:
            PasswordGenerator: PasswordGenerator class
        """
        return PasswordGenerator()

    def test_database_path_creation(self):
        """
        Test if the database path is created correctly.
        """
        data_dir = os.path.dirname(self.db_instance.db_path)
        assert os.path.exists(data_dir), "Database directory should exist."

    def test_table_creation(self):
        """
        Test if the password table is created in the database.
        """
        conn = sqlite3.connect(self.db_instance.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='password';"
        )
        table_exists = cursor.fetchone()
        conn.close()
        assert table_exists is not None, "Table 'password' should exist."

    def test_insert_password(self, pass_gen: PasswordGenerator, name_gen: funkybob):
        """
        Test if a password can be inserted into the database.
        """
        test_password = pass_gen.generate_password(
            random.randint(8, 128),
            include_letters=True,
            include_special=True,
            include_digits=True,
        )
        test_name = next(iter(name_gen))

        self.db_instance.inserting_password(test_name, test_password)

        conn = sqlite3.connect(self.db_instance.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT password FROM password WHERE name = '{test_name}'")
        result = cursor.fetchone()
        conn.close()

        assert result is not None, "Password should be inserted into the database."
        assert result[0] == test_password, (
            "Inserted password should match the test password."
        )

    def test_retrieve_password(self, pass_gen: PasswordGenerator, name_gen: funkybob):
        """
        Test if the inserted password can be retrieved from the database.
        """
        test_password = pass_gen.generate_password(
            random.randint(8, 128),
            include_letters=True,
            include_special=True,
            include_digits=True,
        )
        test_name = next(iter(name_gen))

        self.db_instance.inserting_password(test_name, test_password)

        retrieved_password = self.db_instance.retrieve_password_with_name(test_name)
        assert retrieved_password == test_password, (
            "Retrieved password should match the last inserted password."
        )

    def test_insert_empty_password(self):
        """
        Test if inserting an empty password raises a ValueError.
        """
        with pytest.raises(ValueError, match="Password cannot be empty."):
            self.db_instance.inserting_password("", "")
