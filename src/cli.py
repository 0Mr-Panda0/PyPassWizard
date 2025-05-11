"""
This module provides a command line interface (CLI) for generating passwords.
"""

import os
import click
import logging
import funkybob  # type: ignore
from src.core import PasswordGenerator
from src.utility import Database
from pandera.typing import DataFrame
from dotenv import load_dotenv

load_dotenv()


class CLIApp:
    """
    Command-line interface for managing passwords.
    """

    def __init__(self, path: str):
        """
        Initializes the CLIApp with a PasswordGenerator, Database, and RandomNameGenerator.

        Args:
            path (str): Path to the database file.
        """
        self.password_generator = PasswordGenerator()
        self.database = Database(path)
        self.names_generator = funkybob.RandomNameGenerator()

    def to_bool(self, value: str) -> bool:
        """
        Converts a string value to a boolean.

        Args:
            value (str): The string value ("Yes" or "No").

        Returns:
            bool: The corresponding boolean value.
        """
        return value.lower() == "yes"

    def handle_error(self, error: Exception, message: str) -> None:
        """
        Logs and displays an error message.

        Args:
            error (Exception): The exception that occurred.
            message (str): The error message to display.
        """
        logging.error(f"{message}: {error}")
        click.secho(
            f"{message}: {click.style(str(error), fg='red', bold=True)}", fg="blue"
        )

    def password_generate(
        self,
        length: int,
        include_letters: bool,
        include_special: bool,
        include_digit: bool,
        store: bool,
    ) -> None:
        """
        Generate a password and optionally store it in the database.

        Args:
            length (int): Length of the password to generate (minimum 8, maximum 128).
            include_letters (bool): Whether to include letters in the password.
            include_special (bool): Whether to include special characters in the password.
            include_digit (bool): Whether to include digits in the password.
            store (bool): Whether to store the generated password in the database.
        """
        try:
            password = self.password_generator.generate_password(
                length, include_letters, include_special, include_digit
            )
            if store:
                name = next(iter(self.names_generator))
                self.database.inserting_password(name, password)
                click.secho(
                    f"Password stored with name: {click.style(name, fg='green', bold=True)}",
                    fg="blue",
                )
            else:
                click.secho(
                    f"Generated password: {click.style(password, fg='green', bold=True)}",
                    fg="blue",
                )
        except Exception as e:
            self.handle_error(e, "Error during password generation or storage")

    def retrieve_password(self, name: str) -> None:
        """
        Retrieve the stored password from the database and display it.

        Args:
            name (str): Name associated with the password.
        """
        try:
            password = self.database.retrieve_password_with_name(name)
            click.secho(
                f"Retrieved Password: {click.style(password, fg='green', bold=True)}",
                fg="blue",
            )
        except Exception as e:
            self.handle_error(e, "Error retrieving the password")

    def store_password(self, name: str, password: str) -> None:
        """
        Store a password in the database.

        Args:
            name (str): Name associated with the password.
            password (str): Password to store.
        """
        try:
            self.database.inserting_password(name, password)
            click.secho("Password successfully stored in the database.", fg="green")
        except Exception as e:
            self.handle_error(e, "Error storing password")

    def delete_password(self, name: str) -> None:
        """
        Delete a password from the database.

        Args:
            name (str): Name associated with the password to delete.
        """
        try:
            self.database.delete_password_with_name(name)
            click.secho(f"Password with name: {name} successfully deleted.", fg="green")
        except Exception as e:
            self.handle_error(e, "Error deleting password")

    def save_to_file(
        self, file_location: str, file_name: str, format: str, data: DataFrame
    ) -> None:
        """
        Save passwords to a file in the specified format.

        Args:
            file_location (str): Location to save the file.
            file_name (str): Name of the file.
            format (str): Format of the file (e.g., csv, json, etc.).
            data (DataFrame): Data to save.
        """
        try:
            save_methods = {
                "csv": data.to_csv,
                "xlsx": data.to_excel,
                "md": data.to_markdown,
                "parquet": data.to_parquet,
                "json": data.to_json,
            }
            save_method = save_methods.get(format)
            if save_method:
                save_method(f"{file_location}/{file_name}", index=False)
                click.secho(
                    f"Passwords saved in {click.style(file_location, fg='blue')} as {click.style(file_name, fg='blue')}.",
                    fg="green",
                )
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            self.handle_error(e, "Error occurred while saving/exporting")

    def export_password(self, name: str, format: str, location: str) -> None:
        """
        Export passwords to a file in the specified format and location.

        Args:
            name (str): Name of the output file.
            format (str): Format of the output file.
            location (str): Location to save the file.
        """
        file_name = f"{name}.{format}"
        file_location = os.path.abspath(location)

        try:
            os.makedirs(file_location, exist_ok=True)
            data = self.database.show_all_passwords()
            self.save_to_file(file_location, file_name, format, data)
        except Exception as e:
            self.handle_error(e, "Error exporting passwords")

    def get_command(self) -> click.Group:
        """
        Create the CLI commands.

        Returns:
            click.Group: The CLI command group.
        """

        @click.group()
        @click.version_option(
            version=str(os.getenv("VERSION","0.3.1")),
            prog_name="PyPassWizard",
            message="%(prog)s %(version)s",
        )
        def cli_group():
            """Command line interface for managing passwords."""
            pass

        @cli_group.command()
        @click.option(
            "--length",
            "-l",
            type=int,
            default=12,
            show_default=True,
            help="Length of the password (8-128).",
        )
        @click.option(
            "--include-letters",
            "-c",
            type=click.Choice(["Yes", "No"], case_sensitive=False),
            default="No",
            show_default=True,
            help="Include letters.",
        )
        @click.option(
            "--include-special",
            "-i",
            type=click.Choice(["Yes", "No"], case_sensitive=False),
            default="No",
            show_default=True,
            help="Include special characters.",
        )
        @click.option(
            "--include-digits",
            "-d",
            type=click.Choice(["Yes", "No"], case_sensitive=False),
            default="No",
            show_default=True,
            help="Include digits.",
        )
        @click.option(
            "--store",
            "-s",
            type=click.Choice(["Yes", "No"], case_sensitive=False),
            default="No",
            show_default=True,
            help="Store the password in the database.",
        )
        def generate(
            length: int,
            include_letters: str,
            include_special: str,
            include_digits: str,
            store: str,
        ):
            """Generate a password."""
            self.password_generate(
                length,
                self.to_bool(include_letters),
                self.to_bool(include_special),
                self.to_bool(include_digits),
                self.to_bool(store),
            )

        @cli_group.command()
        @click.option(
            "--name", "-n", required=True, help="Name associated with the password."
        )
        def retrieve(name: str):
            """Retrieve a password."""
            self.retrieve_password(name)

        @cli_group.command()
        @click.option("--name", "-n", required=True, help="Name for the password.")
        @click.option("--password", "-p", required=True, help="Password to store.")
        def store(name: str, password: str):
            """Store a password."""
            self.store_password(name, password)

        @cli_group.command()
        @click.option(
            "--name",
            "-n",
            required=True,
            help="Name associated with the password to delete.",
        )
        def delete(name: str):
            """Delete a password."""
            self.delete_password(name)

        @cli_group.command()
        @click.option("--name", "-n", required=True, help="Name of the output file.")
        @click.option(
            "--format",
            "-f",
            required=True,
            help="Format of the output file (e.g., csv, json).",
        )
        @click.option(
            "--location", "-l", required=True, help="Location to save the file."
        )
        def export(name: str, format: str, location: str):
            """Export passwords."""
            self.export_password(name, format, location)

        return cli_group


def main() -> None:
    """
    Main function to run the CLI application.
    """
    logs_dir = os.getenv("LOGS_DIR", "log")
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, "app.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file)],
    )

    database_path = str(os.getenv("DATABASE_PATH","data/database.db"))
    cli = CLIApp(database_path)
    cli_command = cli.get_command()
    cli_command()


if __name__ == "__main__":
    main()
