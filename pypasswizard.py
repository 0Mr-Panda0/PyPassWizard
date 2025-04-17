from mylib.password_generator import creating_password
from mylib.database_conn import storing_password
import click


@click.command()
@click.option(
    "--l",
    type=int,
    required=True,
    default=11,
    show_default=True,
    help="""\b Password Length""",
)
@click.option(
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
    "--s",
    type=bool,
    required=True,
    default="Yes",
    show_default=True,
    help=f"""\n\b\nStore in Database ?:
1. {click.style("Yes", fg="bright_green")}
2. {click.style("No", fg="bright_red")}\n""",
)
def generate(l=11, sc=True, s=True):
    password = creating_password(l, sc)
    click.echo(f"Your newly generated passoword is : {password}")
    if s is True:
        storing_password(password)


if __name__ == "__main__":
    generate()
