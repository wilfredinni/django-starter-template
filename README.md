# Django starter template

This template provides a comprehensive and easy-to-use starting point for your new project. It comes pre-configured with a robust set of features, saving you the hassle of setting up everything from scratch.

## Key features

- **Django 5+**: Enjoy the latest version of Django with all its features and improvements.
- **PostgreSQL**: Start your project with a robust database without the need to install and configure it.
- **Django Rest Framework**: A powerful and popular toolkit for building Web APIs using Django.
- **Auto Documentation**: Swagger and Redoc auto documentation for your APIs.
- **JWT and Token Authentication**: `dj-rest-auth` for Token and JWT authentication. In development, Basic and Session are also enabled.
- **Custom User Model**: You have the flexibility to define your own fields and behaviors specific to your application's requirements.
- **Django Filters**: You can easily add filters to your views and APIs with `django-filter`.
- **Asynchronous Tasks & Caching**: `Redis`, `Celery`, `django-celery-beat`, `django-celery-results`, and `django-redis` are included for task scheduling and caching.
- **Asynchronous Emails**: The template uses `django-celery-email` for out of the box asynchronous emails.
- **Automatic File Cleanup**: `django-cleanup` is included to automatically delete uploaded files after a database delete.
- **Data Seeding**: You can seed your models with `django-seed`.
- **Debugging & Extensions**: `Django debug toolbar`, `Django extensions` and `Sentry` for debugging and enhancing the functionality of Django.
- **Notebook Support**: Test your queries and code interactively with Jupyter Notebooks.
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
5. Create your super user with `python manage.py createsuperuser`. **Make sure to add the email, as all logins require an email and password**.
6. Run the project with `python manage.py reserver`.
7. Work as usual.