from mylib.password_generator import creating_password
from mylib.database_conn import storing_password
import click


@click.command()
@click.option("--length", default=11, help="password length")
@click.option(
    "--special_character",
    default="Yes",
    help="Wether to allow special character 1. Yes 2. No",
)
@click.option("--store", default="Yes", help="Wether to store locally 1. Yes 2. No")
def generate(length=11, special_character="Yes", store="Yes"):
    """
    Generates a password based on the given parameters and optionally stores it.
    Args:
        length (int, optional): The length of the password to be generated. Defaults to 11.
        special_character (str, optional): Whether to include special characters in the password.
                                           Accepts "Yes" or "No". Defaults to "Yes".
        store (str, optional): Whether to store the generated password. Accepts "Yes" or "No". Defaults to "Yes".
    Returns:
        str: The generated password.
    """
    password = creating_password(length, special_character)
    click.echo(f"Your newly generated passoword is : {password}!")
    if store == "Yes":
        storing_password(password)


if __name__ == "__main__":
    generate()
