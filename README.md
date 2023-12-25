# Django starter template

This template provides a comprehensive and easy-to-use starting point for your new project. It comes pre-configured with a robust set of features, saving you the hassle of setting up everything from scratch.

## Key features

- **Django 4+**: It will be updated to Django 5 when django-celery-beat supports it.
- **Custom User Model & Django Rest Framework**: It includes a custom user model and Django Rest Framework for creating APIs.
- **JWT and Token Authentication**: The template uses `dj-rest-auth` for Token and JWT authentication.
- **Auto Documentation**: `drf-yasg` is included for Swagger and Redoc API auto documentation.
- **Django Filters**: You can easily add filters to your views and APIs with `django-filter`.
- **Asynchronous Tasks & Caching**: `Redis`, `Celery`, `django-celery-beat`, `django-celery-results`, and `django-redis` are included for task scheduling and caching.
- **Asynchronous Emails**: The template uses `django-celery-email` for sending asynchronous emails.
- **Automatic File Cleanup**: `django-cleanup` is included to automatically delete uploaded files after a database delete.
- **Data Seeding**: You can seed your models with `django-seed`.
- **Debugging & Extensions**: The template includes Django debug toolbar and Django extensions for debugging and enhancing.
- **Notebook Support**: Supports Django/Jupiter Notebooks.
- **Error Tracking**: `sentry-sdk` is included for error tracking.
- **Database**: Postgresql as the database.
- **Code Formatting & Testing**: VSCode is configured to use `Black` for code formatting, `pytest` for testing, and `flake8` for linting.

## Requirements

- VSCode
- Docker
- Docker Compose

## How to use

1. Clone the repo or use it as a template to start a new project.
![Use as template](https://docs.github.com/assets/images/help/repository/use-this-template-button.png)
2. Open the project in VSCode.
3. Use `env.example` to create a `.env` file.
4. Hit `CTL/CMD + Shift + p` and select `Reopen in container`. VSCode will create a dev environment, install the dependencies, configure the database and migrate for you.
5. Create your super user with `python manage.py createsuperuser`. Make sure to add the email, as all logins require an email and password.
6. Run the project with `python manage.py reserver`.
7. Work as usual.