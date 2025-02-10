from invoke import task


@task
def install(c):
    c.run("pip install --upgrade pip")
    c.run("pip install -r requirements.txt")


@task
def test(c):
    c.run("python -m pytest -vv --cov=mylib test_*.py")


@task
def format(c):
    c.run("black *.py")


@task
def lint(c):
    c.run("pylint --disable=R,C --ignore-patterns=test_.*?py *.py")


@task(pre=[format, lint])
def refactor(c):
    pass


@task(pre=[install, lint, test, format])
def all(c):
    pass
