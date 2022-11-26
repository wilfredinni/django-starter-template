# Django starter template

An opinionated django template that work best with VSCode DevContainer. Just hit `CTL/CMD + Shift + p` and select `Reopen in container` and the project will create a dev environment, install all the dependencies, configure the database and migrate for you. From there, create your super user, run the project and work as usual.

## Required

- Docker

## What is included

- Django 4+
- Custom User model
- Django Rest Framework
- Token authentication with `dj-rest-auth`
- Swagger and Redoc auto documentation (`drf-yasg`)
- Django filters (`django-filter`)
- `Redis`/`Celery`
- Send emails with Celery (`django-celery-email`)
- Automatically delete uploaded files if an item is deleted from the database (`django-cleanup`)
- Seed your models with `django-seed` (Create 15 custom users: `python manage.py seed users --number=15`)
- Django debug toolbar
- Django extensions
- Support for Django/Jupiter Notebooks.
- Sentry (`sentry-sdk`)
- Postgresql
- Format your code with `Black`
- Test with `pytest`
- Lint with `flake8`