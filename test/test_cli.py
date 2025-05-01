"""
This module contains test cases for the CLI application.
"""

import pytest
import random
import funkybob  # type: ignore
from string import ascii_letters, digits, punctuation
from click.testing import CliRunner
from src.cli import CLIApp


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
        return CLIApp()

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
        """
        name = next(iter(name_gen))

        password = runner.invoke(
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
            ],
        )

        result = runner.invoke(
            cli_app.get_command(),
            [
                "store",
                "-n",
                f"{name}",
                "-p",
                f"{password}",
            ],
        )

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

    def test_store_password(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the storage functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        name = next(iter(name_gen))

        password = runner.invoke(
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
            ],
        )

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

    ##---------------------------------------------------------------------------------------- Testing Delete functionality ------------------------------------------------------------------------------------------

    def test_delete_password(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the delete functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        name = next(iter(name_gen))

        password = runner.invoke(
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

    ##---------------------------------------------------------------------------------------- Testing Retrieve functionality -------------------------------------------------------------------------------------------

    def test_retrieve_password(
        self, runner: CliRunner, cli_app: CLIApp, name_gen: funkybob
    ) -> None:
        """
        Test the storage functionality of the CLI

        Args:
            runner (CliRunner): The CLI runner for invoking commands.
            cli_app (CLIApp): The CLI application instance.
        """
        name = next(iter(name_gen))

        password = runner.invoke(
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
        assert result.output == f"name: {name} password: {password}\n"
