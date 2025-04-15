from mylib.password_generator import creating_password
from mylib.database_conn import storing_password
import click

required_options = {
    1: "l",  # password_length
    2: "sc",  # special_character
    3: "s",  # store_in_database
}


@click.command(context_settings=dict(max_content_width=800))
@click.option(
    "--l",
    required=False,
    type=int,
    default=11,
    help="""\b Password Length (default: 11)""",
)
@click.option(
    "--sc",
    required=False,
    type=bool,
    default="Yes",
    help=f"""\n\b\nAllow Special Character ?:
1. {click.style("Yes", fg="bright_green")}
2. {click.style("No", fg="bright_red")}\n""",
)
@click.option(
    "--s",
    required=False,
    type=bool,
    default="Yes",
    help=f"""\n\b\nStore in Database ?:
1. {click.style("Yes", fg="bright_green")}
2. {click.style("No", fg="bright_red")}\n""",
)
def generate(l=11, sc="Yes", s="Yes"):
    password = creating_password(l, sc)
    click.echo(f"Your newly generated passoword is : {password}!")
    if s == "Yes":
        storing_password(password)


if __name__ == "__main__":
    generate()
