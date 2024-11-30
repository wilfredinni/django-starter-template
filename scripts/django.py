from subprocess import check_call
import os


def runserver():
    check_call(["python", "manage.py", "runserver"])


def makemigrations():
    check_call(["python", "manage.py", "makemigrations"])


def migrate():
    check_call(["python", "manage.py", "migrate"])


def create_dev_env():
    if os.path.exists(".env"):
        print(".env file already exists. Skipping creation.")
        return

    with open(".env", "w") as f:
        f.write(
            "DEBUG=True\n"
            "DJANGO_SECRET_KEY=django-insecure-wlgjuo53y49%-4y5(!%ksylle_ud%b=7%__@9hh+@$d%_^y3s!\n"  # noqa
            "DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres\n"
        )
    print(".env file created successfully.")
