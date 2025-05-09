"""
This module contains test cases for the CLI application.
"""

import pytest
import random
import os
import re
import funkybob  # type: ignore
import pandas as pd  # type: ignore
import sqlite3
from string import ascii_letters, digits, punctuation
from click.testing import CliRunner
from src.cli import CLIApp
from pandera.typing import DataFrame


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
        return CLIApp("data/test.db")

    @pytest.fixture
    def name_gen(self) -> funkybob:
        """
        Fixture for the Name generation.

        Returns:
            funkybob: An instance of funkybob
        """

        return funkybob.RandomNameGenerator()

    ##---------------------------------------------------------------------------------------- Testing Generate functionality ----------------------------------------------------------------------------------------

    def test_generate_password_success(self, runner: CliRunner, cli_app: CLIApp):
        """
        Test the password generation functionality of the CLI.

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        result = runner.invoke(
            cli_app.get_command(),
            [
                "generate",
                "--length",
                f"{random.randint(8, 128)}",
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

    def test_generate_password_no_letters(self, runner: CliRunner, cli_app: CLIApp):
        """
        Test if the Cli app can generate password without alphabets.

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        result = runner.invoke(
            cli_app.get_command(),
            [
                "generate",
                "--length",
                f"{random.randint(8, 128)}",
                "--include-letters",
                "No",
                "--include-special",
                "Yes",
                "--include-digits",
                "Yes",
                "--store",
                "No",
            ],
        )

        assert result.exit_code == 0
        assert ascii_letters not in result.output.split(":")[1]

    def test_generate_password_no_special_characters(
        self, runner: CliRunner, cli_app: CLIApp
    ):
        """
        Test if the Cli app can generate password without special characters.

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        result = runner.invoke(
            cli_app.get_command(),
            [
                "generate",
                "--length",
                f"{random.randint(8, 128)}",
                "--include-letters",
                "Yes",
                "--include-special",
                "No",
                "--include-digits",
                "Yes",
                "--store",
                "No",
            ],
        )

        assert result.exit_code == 0
        assert punctuation not in result.output.split(":")[1]

    def test_generate_password_no_digits(self, runner: CliRunner, cli_app: CLIApp):
        """
        Test if the Cli app can generate password without numericals.

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        result = runner.invoke(
            cli_app.get_command(),
            [
                "generate",
                "--length",
                f"{random.randint(8, 128)}",
                "--include-letters",
                "Yes",
                "--include-special",
                "Yes",
                "--include-digits",
                "No",
                "--store",
                "No",
            ],
        )

        assert result.exit_code == 0
        assert digits not in result.output.split(":")[1]

    def test_generate_password_no_digits_and_no_special_character(
        self, runner: CliRunner, cli_app: CLIApp
    ):
        """
        Test if the Cli app can generate password without special characters or numericals.

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        result = runner.invoke(
            cli_app.get_command(),
            [
                "generate",
                "--length",
                f"{random.randint(8, 128)}",
                "--include-letters",
                "Yes",
                "--include-special",
                "No",
                "--include-digits",
                "No",
                "--store",
                "No",
            ],
        )

        assert result.exit_code == 0
        assert digits not in result.output.split(":")[1]
        assert punctuation not in result.output.split(":")[1]

    def test_generate_password_no_digits_and_no_letters(
        self, runner: CliRunner, cli_app: CLIApp
    ):
        """
        Test if the Cli app can generate password without alphabets or numericals.

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        result = runner.invoke(
            cli_app.get_command(),
            [
                "generate",
                "--length",
                f"{random.randint(8, 128)}",
                "--include-letters",
                "No",
                "--include-special",
                "Yes",
                "--include-digits",
                "No",
                "--store",
                "No",
            ],
        )

        assert result.exit_code == 0
        assert digits not in result.output.split(":")[1]
        assert ascii_letters not in result.output.split(":")[1]

    def test_generate_password_no_letters_and_no_special_character(
        self, runner: CliRunner, cli_app: CLIApp
    ):
        """
        Test if the Cli app can generate password without special characters or digits.

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        result = runner.invoke(
            cli_app.get_command(),
            [
                "generate",
                "--length",
                f"{random.randint(8, 128)}",
                "--include-letters",
                "No",
                "--include-special",
                "No",
                "--include-digits",
                "Yes",
                "--store",
                "No",
            ],
        )

        assert result.exit_code == 0
        assert ascii_letters not in result.output.split(":")[1]
        assert punctuation not in result.output.split(":")[1]

    def test_generate_password_with_alternate_tags(
        self, runner: CliRunner, cli_app: CLIApp
    ):
        """
        Test if the Cli app can generate password without special characters or digits.

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        result = runner.invoke(
            cli_app.get_command(),
            [
                "generate",
                "-l",
                f"{random.randint(8, 128)}",
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

        assert result.exit_code == 0
        assert "Generated password:" in result.output

    def test_generate_password_invalid_special_flag(
        self, runner: CliRunner, cli_app: CLIApp
    ):
        """
        Test the password generation functionality of the CLI with an invalid special flag.

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        result = runner.invoke(
            cli_app.get_command(),
            [
                "generate",
                "--length",
                f"{random.randint(8, 128)}",
                "-include-letter",
                "Yes",
                "--include-special",
                "Invalid",  # Invalid value
                "--include-digits",
                "Yes",
                "--store",
                "No",
            ],
        )

        assert result.exit_code != 0
        assert "Invalid value for '--include-special'" in result.output

    ##---------------------------------------------------------------------------------------- Testing Store functionality ----------------------------------------------------------------------------------------
    def test_store_password_with_tags(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the storage functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
            name_gen (funkybob): The name generator.
        """

        ## Generate name and password

        name = next(iter(name_gen))

        password = (
            runner.invoke(
                cli_app.get_command(),
                [
                    "generate",
                    "-l",
                    f"{random.randint(8, 128)}",
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

        result = runner.invoke(
            cli_app.get_command(),
            ["store", "-n", f"{name}", "-p", f"{password}"],
        )

        ret_pass = (
            runner.invoke(
                cli_app.get_command(),
                ["retrieve", "-n", f"{name}"],
            )
        ).output.split(" ")[3]

        runner.invoke(
            cli_app.get_command(),
            [
                "delete",
                "-n",
                f"{name}",
            ],
        )

        assert result.exit_code == 0
        assert result.output == "Password sucessfully stored in the database.\n"
        assert ret_pass.rstrip(".\n") == password.rstrip()

    def test_store_password(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the storage functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
            name_gen (funkybob): The name generator.
        """
        name = next(iter(name_gen))

        password = (
            runner.invoke(
                cli_app.get_command(),
                [
                    "generate",
                    "-l",
                    f"{random.randint(8, 128)}",
                    "--include-letters",
                    "Yes",
                    "--include-special",
                    "Yes",
                    "-include-digits",
                    "Yes",
                    "--store",
                    "No",
                ],
            )
        ).output.split(" ")[2]

        result = runner.invoke(
            cli_app.get_command(),
            [
                "store",
                "--name",
                f"{name}",
                "--password",
                f"{password}",
            ],
        )

        ret_pass = (
            runner.invoke(
                cli_app.get_command(),
                ["retrieve", "-n", f"{name}"],
            )
        ).output.split(" ")[3]

        runner.invoke(
            cli_app.get_command(),
            [
                "delete",
                "-n",
                f"{name}",
            ],
        )

        assert result.exit_code == 0
        assert result.output == "Password sucessfully stored in the database.\n"
        assert ret_pass.rstrip(".\n") == password

    ##---------------------------------------------------------------------------------------- Testing Delete functionality ------------------------------------------------------------------------------------------

    def test_delete_password(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the delete functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
            name_gen (funkybob): The name generator.
        """
        name = next(iter(name_gen))

        password = (
            runner.invoke(
                cli_app.get_command(),
                [
                    "generate",
                    "-l",
                    f"{random.randint(8, 128)}",
                    "--c",
                    "Yes",
                    "--i",
                    "Yes",
                    "--d",
                    "Yes",
                ],
            )
        ).output.split(" ")[2]

        runner.invoke(
            cli_app.get_command(),
            [
                "store",
                "--name",
                f"{name}",
                "--password",
                f"{password}",
            ],
        )

        result = runner.invoke(
            cli_app.get_command(),
            [
                "delete",
                "--name",
                f"{name}",
            ],
        )

        assert result.exit_code == 0
        assert result.output == f"Password with name: {name} sucessfully deleted.\n"

        isDeleted = runner.invoke(
            cli_app.get_command(),
            [
                "retrieve",
                "--name",
                f"{name}",
            ],
        )

        assert isDeleted.output == "No passwords found in the database.\n"

    ##---------------------------------------------------------------------------------------- Testing Retrieve functionality -------------------------------------------------------------------------------------------

    def test_retrieve_password(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the storage functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
            name_gen (funkybob): The name generator.
        """
        name = next(iter(name_gen))

        password = (
            runner.invoke(
                cli_app.get_command(),
                [
                    "generate",
                    "-l",
                    f"{random.randint(8, 128)}",
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
                f"{name}",
                "--password",
                f"{password}",
            ],
        )

        result = runner.invoke(
            cli_app.get_command(),
            [
                "retrieve",
                "--name",
                f"{name}",
            ],
        )

        runner.invoke(
            cli_app.get_command(),
            [
                "delete",
                "--name",
                f"{name}",
            ],
        )

        assert result.exit_code == 0
        assert result.output == f"name: {name} password: {password}.\n"

    ##---------------------------------------------------------------------------------------- Testing Export functionality -------------------------------------------------------------------------------------------

    def test_export_password_csv(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the export functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
            name_gen (funkybob): The name generator.
        """
        name = next(iter(name_gen))

        password = (
            runner.invoke(
                cli_app.get_command(),
                [
                    "generate",
                    "-l",
                    f"{random.randint(8, 128)}",
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
                f"{name}",
                "--password",
                f"{password}",
            ],
        )

        result = runner.invoke(
            cli_app.get_command(),
            [
                "export",
                "--name",
                "output",
                "--format",
                "csv",
                "--location",
                "passwords",
            ],
        )

        file_name = "output.csv"
        file_location = os.path.abspath("passwords")

        assert result.exit_code == 0
        assert (
            result.output
            == f"Passwords saved in location {file_location} inside {file_name}.\n"
        )

        target_df = pd.read_csv(os.path.join(file_location, file_name))

        conn = sqlite3.connect("data/test.db")
        query = "SELECT * FROM password"
        source_df = pd.read_sql_query(query, conn)
        source_df.drop("id", axis=1, inplace=True)

        assert source_df.equals(target_df), "False"
        conn.close()

        file_to_be_deleted = os.path.join(file_location, file_name)
        os.remove(file_to_be_deleted)
        os.rmdir(file_location)

    def test_export_password_excel(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the export functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
            name_gen (funkybob): The name generator.
        """
        name = next(iter(name_gen))

        password = (
            runner.invoke(
                cli_app.get_command(),
                [
                    "generate",
                    "-l",
                    f"{random.randint(8, 128)}",
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
                f"{name}",
                "--password",
                f"{password}",
            ],
        )

        result = runner.invoke(
            cli_app.get_command(),
            [
                "export",
                "--name",
                "output",
                "--format",
                "xlsx",
                "--location",
                "passwords",
            ],
        )

        file_name = "output.xlsx"
        file_location = os.path.abspath("passwords")

        assert result.exit_code == 0
        assert (
            result.output
            == f"Passwords saved in location {file_location} inside {file_name}.\n"
        )
        target_df = pd.read_excel(os.path.join(file_location, file_name))

        conn = sqlite3.connect("data/test.db")
        query = "SELECT * FROM password"
        source_df = pd.read_sql_query(query, conn)
        source_df.drop("id", axis=1, inplace=True)

        assert source_df.equals(target_df), "False"
        conn.close()

        file_to_be_deleted = os.path.join(file_location, file_name)
        os.remove(file_to_be_deleted)
        os.rmdir(file_location)

    def markdown_to_dataframe(self, file_location: str, file_name: str) -> DataFrame:
        """Convert from markdown to dataframe

        Args:
            file_location (str): location of the markdown file
            file_name (str): name of the markdoen file

        Returns:
            DataFrame: returned dataframe
        """
        with open(
            os.path.join(file_location, file_name), "r", encoding="utf-8"
        ) as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines if "---" not in line]

        headers = [h.strip() for h in lines[0].split("|")[1:-1]]

        data = []
        for line in lines[1:]:
            values = [
                val.strip() for val in re.split(r"([^|]+(?:\|[^|]+)*)", line)[1:-1]
            ]
            data.append(values)

        final_data = []
        for i in data:
            final_data.append(
                [i[0].split("| ")[0].strip(), i[0].split("| ")[1].strip() + "\n"]
            )

        return pd.DataFrame(final_data, columns=headers)

    def test_export_password_md(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the export functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
            name_gen (funkybob): The name generator.
        """
        name = next(iter(name_gen))

        password = (
            runner.invoke(
                cli_app.get_command(),
                [
                    "generate",
                    "-l",
                    f"{random.randint(8, 128)}",
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
                f"{name}",
                "--password",
                f"{password}",
            ],
        )

        result = runner.invoke(
            cli_app.get_command(),
            [
                "export",
                "--name",
                "output",
                "--format",
                "md",
                "--location",
                "passwords",
            ],
        )

        file_name = "output.md"
        file_location = os.path.abspath("passwords")

        assert result.exit_code == 0
        assert (
            result.output
            == f"Passwords saved in location {file_location} inside {file_name}.\n"
        )

        target_df = self.markdown_to_dataframe(file_location, file_name)

        conn = sqlite3.connect("data/test.db")
        query = "SELECT * FROM password"
        source_df = pd.read_sql_query(query, conn)
        source_df.drop("id", axis=1, inplace=True)

        assert source_df.equals(target_df), "False"
        conn.close()

        file_to_be_deleted = os.path.join(file_location, file_name)
        os.remove(file_to_be_deleted)
        os.rmdir(file_location)

    def test_export_password_json(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the export functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
            name_gen (funkybob): The name generator.
        """
        name = next(iter(name_gen))

        password = (
            runner.invoke(
                cli_app.get_command(),
                [
                    "generate",
                    "-l",
                    f"{random.randint(8, 128)}",
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
                f"{name}",
                "--password",
                f"{password}",
            ],
        )

        result = runner.invoke(
            cli_app.get_command(),
            [
                "export",
                "--name",
                "output",
                "--format",
                "json",
                "--location",
                "passwords",
            ],
        )

        file_name = "output.json"
        file_location = os.path.abspath("passwords")

        assert result.exit_code == 0
        assert (
            result.output
            == f"Passwords saved in location {file_location} inside {file_name}.\n"
        )

        target_df = pd.read_json(os.path.join(file_location, file_name))

        conn = sqlite3.connect("data/test.db")
        query = "SELECT * FROM password"
        source_df = pd.read_sql_query(query, conn)
        source_df.drop("id", axis=1, inplace=True)

        assert source_df.equals(target_df), "False"
        conn.close()

        file_to_be_deleted = os.path.join(file_location, file_name)
        os.remove(file_to_be_deleted)
        os.rmdir(file_location)

    def test_export_password_parquet(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the export functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
            name_gen (funkybob): The name generator.
        """
        name = next(iter(name_gen))

        password = (
            runner.invoke(
                cli_app.get_command(),
                [
                    "generate",
                    "-l",
                    f"{random.randint(8, 128)}",
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
                f"{name}",
                "--password",
                f"{password}",
            ],
        )

        result = runner.invoke(
            cli_app.get_command(),
            [
                "export",
                "--name",
                "output",
                "--format",
                "parquet",
                "--location",
                "passwords",
            ],
        )

        file_name = "output.parquet"
        file_location = os.path.abspath("passwords")

        assert result.exit_code == 0
        assert (
            result.output
            == f"Passwords saved in location {file_location} inside {file_name}.\n"
        )

        target_df = pd.read_parquet(os.path.join(file_location, file_name))

        conn = sqlite3.connect("data/test.db")
        query = "SELECT * FROM password"
        source_df = pd.read_sql_query(query, conn)
        source_df.drop("id", axis=1, inplace=True)

        assert source_df.equals(target_df), "False"
        conn.close()

        file_to_be_deleted = os.path.join(file_location, file_name)
        os.remove(file_to_be_deleted)
        os.rmdir(file_location)
