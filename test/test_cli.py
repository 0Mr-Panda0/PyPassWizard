"""
This module contains test cases for the CLI application.
"""

import pytest
import os
import pandas as pd  # type: ignore
import sqlite3
import re
from click.testing import CliRunner
from src.cli import CLIApp
from pandera.typing import DataFrame
from dotenv import load_dotenv

load_dotenv()

class TestCLIApp:

    @pytest.fixture
    def runner(self) -> CliRunner:
        """
        Fixture for the CLI runner.

        Returns:
            CliRunner: A test runner for invoking CLI commands.
        """
        return CliRunner()

    @pytest.fixture
    def cli_app(self) -> CLIApp:
        """
        Fixture for the CLI application.

        Returns:
            CLIApp: An instance of the CLI application.
        """
        return CLIApp(str(os.getenv('TEST_DB_PATH')))

    def generate_and_store_password(
        self, runner: CliRunner, cli_app: CLIApp, name: str
    ) -> str:
        """
        Helper method to generate and store a password.

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
            name (str): The name to associate with the password.

        Returns:
            str: The generated password.
        """
        password = (
            runner.invoke(
                cli_app.get_command(),
                [
                    "generate",
                    "-l",
                    "12",
                    "-c",
                    "Yes",
                    "-i",
                    "Yes",
                    "-d",
                    "Yes",
                    "-s",
                    "No",
                ],
            )
        ).output.split(" ")[2]

        runner.invoke(
            cli_app.get_command(),
            [
                "store",
                "--name",
                name,
                "--password",
                password,
            ],
        )

        return password

    def cleanup_exported_files(self, file_location: str, file_name: str) -> None:
        """
        Helper method to clean up exported files.

        Args:
            file_location (str): The location of the exported file.
            file_name (str): The name of the exported file.
        """
        file_to_be_deleted = os.path.join(file_location, file_name)
        if os.path.exists(file_to_be_deleted):
            os.remove(file_to_be_deleted)
        if os.path.exists(file_location):
            os.rmdir(file_location)

    def test_generate_password_success(self, runner: CliRunner, cli_app: CLIApp):
        """
        Test the password generation functionality of the CLI.
        """
        result = runner.invoke(
            cli_app.get_command(),
            [
                "generate",
                "--length",
                "12",
                "--include-letters",
                "Yes",
                "--include-special",
                "Yes",
                "--include-digits",
                "Yes",
                "--store",
                "No",
            ],
        )

        assert result.exit_code == 0
        assert "Generated password:" in result.output

    def test_store_and_retrieve_password(self, runner: CliRunner, cli_app: CLIApp) -> None:
        """
        Test the storage and retrieval functionality of the CLI.
        """
        name = "test_name"
        password = self.generate_and_store_password(runner, cli_app, name)

        result = runner.invoke(
            cli_app.get_command(),
            [
                "retrieve",
                "--name",
                name,
            ],
        )

        runner.invoke(
            cli_app.get_command(),
            [
                "delete",
                "--name",
                name,
            ],
        )

        assert result.exit_code == 0
        assert f"Retrieved Password: {password}\n" in result.output

    def test_delete_password(self, runner: CliRunner, cli_app: CLIApp) -> None:
        """
        Test the delete functionality of the CLI.
        """
        name = "test_name"
        self.generate_and_store_password(runner, cli_app, name)

        result = runner.invoke(
            cli_app.get_command(),
            [
                "delete",
                "--name",
                name,
            ],
        )

        assert result.exit_code == 0
        assert f"Password with name: {name} successfully deleted." in result.output

        is_deleted = runner.invoke(
            cli_app.get_command(),
            [
                "retrieve",
                "--name",
                name,
            ],
        )

        assert "No password associated with name:" in is_deleted.output

    def read_markdown(self, file_location: str) -> DataFrame:
        """
        Convert from markdown to dataframe

        Args:
            file_location (str): location of the markdown file
            file_name (str): name of the markdoen file

        Returns:
            DataFrame: returned dataframe
        """
        with open(file_location, "r", encoding="utf-8") as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines if "---" not in line]

        headers = [h.strip() for h in lines[0].split("|")[1:-1]]

        data = []
        for line in lines[1:]:
            values = [val.strip() for val in re.split(r"([^|]+(?:\|[^|]+)*)", line)[1:-1]]
            data.append(values)

        final_data = []
        for i in data:
            final_data.append([i[0].split("| ")[0].strip(), i[0].split("| ")[1].strip() + "\n"])

        return pd.DataFrame(final_data, columns=headers)

    @pytest.mark.parametrize("format", ["csv", "xlsx", "json", "parquet", "md"])
    def test_export_password(self, runner: CliRunner, cli_app: CLIApp, format: str) -> None:
        """
        Test the export functionality of the CLI for various formats.

        Args:
            format (str): The format to export the passwords (e.g., csv, xlsx, json, parquet).
        """
        name = "test_name"
        self.generate_and_store_password(runner, cli_app, name)

        result = runner.invoke(
            cli_app.get_command(),
            [
                "export",
                "--name",
                "output",
                "--format",
                format,
                "--location",
                str(os.getenv('TEST_EXPORT_DIR')),
            ],
        )

        file_name = f"output.{format}"
        file_location = os.path.abspath(str(os.getenv('TEST_EXPORT_DIR')))

        assert result.exit_code == 0
        assert (
            result.output
            == f"Passwords saved in {file_location} as {file_name}.\n"
        )

        # Validate exported data
        if format == "csv":
            target_df = pd.read_csv(os.path.join(file_location, file_name))
        elif format == "xlsx":
            target_df = pd.read_excel(os.path.join(file_location, file_name))
        elif format == "json":
            target_df = pd.read_json(os.path.join(file_location, file_name))
        elif format == "parquet":
            target_df = pd.read_parquet(os.path.join(file_location, file_name))
        elif format == "md":
            target_df = self.read_markdown(os.path.join(file_location, file_name))

        conn = sqlite3.connect(str(os.getenv('TEST_DB_PATH')))
        query = "SELECT name, password FROM password"
        source_df = pd.read_sql_query(query, conn)
        conn.close()

        assert source_df.equals(target_df), "Exported data does not match database data."

        # Clean up exported files
        self.cleanup_exported_files(file_location, file_name)

        # Delete the test password
        runner.invoke(
            cli_app.get_command(),
            [
                "delete",
                "--name",
                name,
            ],
        )

        # Clean up the test database
        if os.path.exists(str(os.getenv('TEST_DB_PATH'))):
            os.remove(str(os.getenv('TEST_DB_PATH')))
        # Clean up the test export directory
        if os.path.exists(str(os.getenv('TEST_EXPORT_DIR'))):
            os.rmdir(str(os.getenv('TEST_EXPORT_DIR')))
        # Clean database path
        if os.path.exists(str(os.getenv('TEST_DB_PATH')).split("/")[0]):
            os.rmdir(str(os.getenv('TEST_DB_PATH')).split("/")[0])

