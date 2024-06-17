from mylib.password_generator import creating_password, storing_password
import click


@click.command()
@click.option("--length", default=11, help="password length")
@click.option(
    "--special_character",
    default="Yes",
    help="Wether to allow special character 1. Yes 2. No",
)
@click.option(
    "--store",
    default="Yes",
    help="Wether to store locally 1. Yes 2. No",
)
def generate(length=11, special_character="Yes", store="Yes"):
    """Simple program generate to generate password with variable length"""
    password = creating_password(length, special_character)
    click.echo(f"Your newly generated passoword is : {password}!")
    if store == "Yes":
        storing_password(password)


if __name__ == "__main__":
    generate()
