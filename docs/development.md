# Development Guide

This guide provides detailed instructions for setting up your development environment, running the application, and utilizing the various features of the Django Starter Template.

## Quick Start

### Prerequisites

*   **VS Code**: The recommended code editor.
*   **Docker**: For containerizing the application.
*   **Docker Compose**: For managing multi-container Docker applications.

### Setup Steps

1.  **Use the Template**: Click the "Use this template" button on the GitHub repository page to create your own repository.
2.  **Open in VS Code**: Clone your new repository and open it in Visual Studio Code.
3.  **Reopen in Container**: Open the command palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and select "Remote-Containers: Reopen in Container". This will build the development container and install all the necessary dependencies.
4.  **Create a Superuser**: Once the container is running, open a new terminal in VS Code and run the following command to create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

5.  **Start the Server**: Start the Django development server:

    ```bash
    python manage.py runserver
    ```

## Useful Commands

This section provides a list of useful commands to help you manage and develop your Django project efficiently.

### Celery Tasks

*   `poetry run worker`: to start a new Celery worker.
*   `poetry run beat`: to start your periodic tasks.

### Test commands:

*   `pytest` to run the tests.
*   `pytest --cov` to run the tests with coverage.
*   `pytest --cov --cov-report=html` to run the tests with coverage and generate a HTML report.

### You can also use

*   `poetry run server` instead of `python manage.py runserver`
*   `poetry run makemigrations` instead of `python manage.py makemigrations`
*   `poetry run migrate` instead of `python manage.py migrate`
*   `poetry run create_dev_env` to create a development `.env` file
*   `poetry run seed` to seed your database with sample data

### Database Seeding

The template includes a powerful seeding command to populate your database with sample data for development and testing:

```bash
# Basic seeding with default options (creates 10 users)
python manage.py seed

# Create specific number of users
python manage.py seed --users 20

# Create a superuser (admin@admin.com:admin)
python manage.py seed --superuser

# Clean existing data before seeding
python manage.py seed --clean

# Combine options
python manage.py seed --users 50 --superuser --clean
```

## Environment Setup

*   **Development**: A `.env` file is created automatically when you run `poetry run create_dev_env` or when you first open the project in the dev container.
*   **Production**: See the `.env.example` file for the required environment variables.