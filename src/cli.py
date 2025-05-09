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


class CLIApp:
    """
    This class provides methods to generate passwords with various options,
    store them in a database, and retrieve the stored password associated with a name and delete a password associated with a name.
    """

    def __init__(self, path: str):
        """
        This method sets up the PasswordGenerator, Database and funkybob instances.

        Args:
            path (str): path to Database
        """
        self.password_generator = PasswordGenerator()
        self.database = Database(path)
        self.names_generator = funkybob.RandomNameGenerator()

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
            length (int): length of the password to generate (minimum 8, maximum 128).
            include_letters (bool): wether to include letters in the password.
            include_special (bool): wether to include special characters in the password.
            include_digit (bool): wether to include digits in the password.
            store (bool): wether to store the generated password in the database.
        """
        try:
            password = self.password_generator.generate_password(
                length, include_letters, include_special, include_digit
            )

            click.secho(f"Generated password: {password}", fg="blue", bold=True)

            if store:
                self.database.inserting_password(
                    next(iter(self.names_generator)), password
                )
                click.secho("Password successfully stored in the database.", fg="green")

        except Exception as e:
            logging.error(f"Error during password generation or storage: {e}")
            click.secho(f"An error occurred: {e}", fg="red")

    def retrieve_password(self, name: str) -> None:
        """
        Retrieve the stored password from the database and display it using the name provided.

        Args:
            name (str): name associated with the password.
        """
        try:
            password = self.database.retrieve_password_with_name(name)
            if password:
                click.secho(f"name: {name} password: {password}.", fg="blue", bold=True)
            else:
                click.secho("No passwords found in the database.", fg="yellow")
        except Exception as e:
            logging.error(f"Error retrieving the password: {e}")
            click.secho(f"An error occurred: {e}", fg="red")

    def store_password(self, name: str, password: str) -> None:
        """
        Storing password for a given name.

        Args:
            name (str): name associated with the password.
            password (str): password generated for this name.
        """
        try:
            self.database.inserting_password(name, password)
            click.secho("Password sucessfully stored in the database.", fg="green")
        except Exception as e:
            logging.error(f"Error storing password: {e}")
            click.secho(f"An error occurred: {e}", fg="red")

    def delete_password(self, name: str) -> None:
        """
        Deleting the password stored for the following name.

        Args:
            name (str): name for which the password is set.
        """
        try:
            self.database.delete_password_with_name(name)
            click.secho(f"Password with name: {name} sucessfully deleted.", fg="green")
        except Exception as e:
            logging.error(f"Error in deleting password: {e}")
            click.secho(f"An error occurred: {e}", fg="red")

    def gen_pass(
        self,
        length: int,
        include_letters: str,
        include_special: str,
        include_digits: str,
        store: str,
    ) -> None:
        """
        Command line interface for generating a password.

        Args:
            length (int): length of the password to generate (minimum 8, maximum 128).
            include_letters (str): wether to include letters in the password.
            include_special (str): wether to include special characters in the password.
            include_digits (str): wether to include digits in the password.
            store (str): wether to store the generated password in the database.
        """
        store_bool = store.lower() == "yes"
        include_special_bool = include_special.lower() == "yes"
        include_digits_bool = include_digits.lower() == "yes"
        include_letters_bool = include_letters.lower() == "yes"
        self.password_generate(
            length,
            include_letters_bool,
            include_special_bool,
            include_digits_bool,
            store_bool,
        )

    def save_to_file(
        self,
        file_location: str,
        file_name: str,
        format: str,
        location_styled: str,
        file_name_styled: str,
        data: DataFrame,
    ):
        """Save files in specific formats

        Args:
            file_location (str): location of files.
            file_name (str): name of file.
            format (str): formmat of file.
            location_styled (str): styled file location.
            file_name_styled (str): styled file name.
            data (DataFrame): data in dataframe format.
        """

        try:
            if format == "csv":
                data.to_csv(f"{file_location}/{file_name}", index=False)
            if format == "xlsx":
                data.to_excel(f"{file_location}/{file_name}", index=False)
            if format == "md":
                data.to_markdown(f"{file_location}/{file_name}", index=False)
            if format == "parquet":
                data.to_parquet(f"{file_location}/{file_name}", index=False)
            if format == "json":
                data.to_json(f"{file_location}/{file_name}", index=False)
            logging.info(
                f"Passwords saved in location {file_location} inside {file_name}"
            )
            click.secho(
                f"Passwords saved in location {location_styled} inside {file_name_styled}.",
                fg="green",
            )
        except Exception as e:
            logging.error(f"Error occured while saving exporting : {e}")
            click.secho(f"Error occured while saving exporting : {e}", fg="red")

    def export_password(self, name: str, format: str, location: str):
        """
        Exporting Password in specified format and location.

        Args:
            name (str): name of the output file.
            format (str): format you want your passwords in.
            location (str): location of the password.
        """
        file_name = f"{name}.{format}"
        file_location = os.path.abspath(location)

        try:
            if not os.path.exists(file_location):
                os.makedirs(file_location)
                logging.info(f"Created directory: {file_location}")
        except Exception as e:
            logging.error(f"Error in creating the location directory: {e}")

        data = self.database.show_all_passwords()
        location_styled = click.style(f"{file_location}", fg="blue")
        file_name_styled = click.style(f"{file_name}", fg="blue")
        self.save_to_file(
            file_location, file_name, format, location_styled, file_name_styled, data
        )

    def get_command(self) -> click.Group:
        """
        Command line interface for generating a password.

        Returns:
            click.Group: Command line interface for generating a password.
        """

        @click.group()
        def cli_group():
            """
            Command line interface for generating a password.
            """
            pass

        @cli_group.command()
        @click.option(
            "--length",
            "-l",
            type=int,
            prompt="Enter length of the password (minimum 8, maximum 128)",
            required=True,
            default=12,
            show_default=True,
            help="Length of the password to generate (minimum 8, maximum 128).",
        )
        @click.option(
            "--include-letters",
            "-c",
            type=click.Choice(["Yes", "No"], case_sensitive=False),
            prompt="Do you want to include lowercase and uppercase english alphabets in your password?",
            required=False,
            default="No",
            show_default=True,
            help="Include letters in the password.",
        )
        @click.option(
            "--include-special",
            "-i",
            type=click.Choice(["Yes", "No"], case_sensitive=False),
            prompt="Do you want to include special characters in your password?",
            required=False,
            default="No",
            show_default=True,
            help="Include special characters in the password.",
        )
        @click.option(
            "--include-digits",
            "-d",
            type=click.Choice(["Yes", "No"], case_sensitive=False),
            prompt="Do you want to include digits in your password?",
            required=False,
            default="No",
            show_default=True,
            help="Include digits in the password.",
        )
        @click.option(
            "--store",
            "-s",
            type=click.Choice(["Yes", "No"], case_sensitive=False),
            prompt="Do you want to save the password to the database?",
            required=True,
            default="No",
            show_default=True,
            help="Store the generated password in the database.",
        )
        def generate(
            length: int,
            include_letters: str,
            include_special: str,
            include_digits: str,
            store: str,
        ) -> None:
            """
            Generate a password and optionally store it in the database.

            Args:
                length (int): length of the password to generate (minimum 8, maximum 128).
                include_letters (str): wether to include letters in the password.
                include_special (str): wether to include special characters in the password.
                include_digits (str): wether to include digits in the password.
                store (str): wether to store the generated password in the database.
            """
            self.gen_pass(
                length, include_letters, include_special, include_digits, store
            )

        @cli_group.command()
        @click.option(
            "--name",
            "-n",
            required=True,
            prompt="Enter the name associated with the password",
            help="Name which is associated with the password",
        )
        def retrieve(name: str) -> None:
            """
            Retrieve the stored password from the database and display it.

            Args:
                name (str): name of the password
            """
            self.retrieve_password(name)

        @cli_group.command()
        @click.option(
            "--name",
            "-n",
            required=True,
            prompt="Enter the name associated with the password",
            help="Name for a password you want to store.",
        )
        @click.option(
            "--password",
            "-p",
            required=True,
            prompt="Enter the password associated with the name",
            help="Password you want to store with this name.",
        )
        def store(name: str, password: str) -> None:
            """
            Store already generated password with a name.

            Args:
                name (str): name of the password.
            """
            self.store_password(name, password)

        @cli_group.command()
        @click.option(
            "--name",
            "-n",
            required=True,
            prompt="Enter the name associated with the password which you want to delete",
            help="Name for a password you want to store.",
        )
        def delete(name: str):
            """
            Deletes the password with the following name.

            Args:
                name (str): name of the password you want to delete.
            """
            self.delete_password(name)

        @cli_group.command()
        @click.option(
            "--name",
            "-n",
            required=True,
            prompt="Enter the name of the file you want to export your passwords in.",
            help="Exporting all your passwords using this file name.",
        )
        @click.option(
            "--format",
            "-f",
            required=True,
            prompt="Enter the format you want to export your passwords in.",
            help="Exporting all your stored passwords in specifiec format.",
        )
        @click.option(
            "--location",
            "-l",
            required=True,
            prompt="Enter the location you want to export your passwords in.",
            help="Exporting all your stored passwords in specifiec location.",
        )
        def export(name: str, format: str, location: str):
            """Exporting stored password in specified password.

            Args:
                name (str): namr of the file.
                format (str): format you want your password in.
                location (str): location of the export file.
            """
            self.export_password(name, format, location)

        return cli_group


def main() -> None:
    """
    Main function to run the CLI application.
    This function sets up the logging configuration and initializes the CLI application.
    """
    # Ensure the logs directory exists
    logs_dir = os.path.join(os.path.dirname(__file__), "../log")
    os.makedirs(logs_dir, exist_ok=True)

    # Configure logging to write only to a file
    log_file = os.path.join(logs_dir, "app.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file)  # Log only to the file
        ],
    )

    cli = CLIApp("data/database.db")
    cli_command = cli.get_command()
    cli_command()


if __name__ == "__main__":
    main()
