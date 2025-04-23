"""
Script to automate the process entire build process.
"""

from invoke import task


@task
def install(c):
    """
    installing and updating dependencies.
    """
    c.run("python -m pip install --upgrade pip && pip install -r requirements.txt")


@task
def test(c):
    """
    Running test script to check if code is breaking.
    """
    c.run("python -m pytest -vv --cov=src test/test_pypasswizard.py")


@task
def design(c):
    """
    formatting code.
    """
    c.run("black src/ test/ *.py")


@task
def lint(c):
    """
    linting code.
    """
    c.run("pylint --disable=R,C src/ test/ *.py")


@task(pre=[install, lint, design, test])
def build(c):
    """
    building the code.
    """
    c.run("echo Build completed.")
