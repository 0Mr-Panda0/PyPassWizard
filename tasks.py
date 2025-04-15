from invoke import task
import os


@task
def setup(c):
    c.run("echo Setting up the project...")
    location = input("Enter the location to store passwords:")
    if not os.path.exists(location) and not os.path.exists(".env"):
        print(f"Directory {location} and file .env does not exist. Creating them.")
        os.makedirs(location)
        with open(".env", "w", encoding="utf-8") as env_file:
            env_file.write(f"DB_PATH={location}/database.db")
    else:
        pass


@task
def install(c):
    c.run("python -m pip install --upgrade pip && pip install -r requirements.txt")


@task
def test(c):
    c.run("python -m pytest -vv --cov=mylib test_app.py")


@task
def design(c):
    c.run("black *.py")


@task
def lint(c):
    c.run("pylint --disable=R,C --ignore-patterns=test_.*?py *.py")


@task(pre=[setup, install, lint, design, test])
def build(c):
    c.run("echo Build completed.")


@task(pre=[build])
def run(c):
    c.run("python app.py --help")
