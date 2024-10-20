from subprocess import check_call


def runserver():
    check_call(["python", "manage.py", "runserver"])


def makemigrations():
    check_call(["python", "manage.py", "makemigrations"])


def migrate():
    check_call(["python", "manage.py", "migrate"])
