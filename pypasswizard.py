"""
Cli tool to generate password
"""

import click
from src.password_generator import creating_password
from src.database_connetion import storing_password


@click.command()
@click.option(
    "--length",
    "--l",
    type=int,
    required=True,
    default=11,
    show_default=True,
    help="""\b Password Length""",
)
@click.option(
    "--special_character",
    "--sc",
    type=bool,
    required=True,
    default="Yes",
    show_default=True,
    help=f"""\n\b\nAllow Special Character ?:
1. {click.style("Yes", fg="bright_green")}
2. {click.style("No", fg="bright_red")}\n""",
)
@click.option(
    "--store",
    "--s",
    type=bool,
    required=True,
    default="Yes",
    show_default=True,
    help=f"""\n\b\nStore in Database ?:
1. {click.style("Yes", fg="bright_green")}
2. {click.style("No", fg="bright_red")}\n""",
)
def main(length=11, special_character=True, store=True):
    """
    cli input of password length, special character and storage then creates password and stores it.
    """
    password = creating_password(length, special_character)
    click.secho(f"Your newly generated passoword is : {password}", bold=True)
    if store is True:
        storing_password(password)


if __name__ == "__main__":
    main()
