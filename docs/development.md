# Development Workflow

## Overview

This guide outlines the essential commands and best practices for developing your application within the Django Starter Template. It assumes you have completed the initial environment setup, ideally using the provided Dev Container.

## Core Development Commands

The project provides a set of convenient `poetry run` commands to streamline common development tasks. These commands should be executed from your terminal within the VS Code Dev Container or your activated Poetry shell.

The project includes convenient scripts in `pyproject.toml` to simplify common development tasks. You should use these `poetry run` commands from the terminal inside your VS Code dev container.

| Command | Description |
| :--- | :--- |
| `poetry run server` | Starts the Django development server. |
| `poetry run makemigrations` | Creates new database migrations based on model changes. |
| `poetry run migrate` | Applies pending database migrations. |
| `poetry run test` | Runs the test suite using `pytest`. |
| `poetry run test-cov`| Runs the test suite and generates a coverage report. |

### Testing

The project utilizes `pytest` for its test suite. Below are common commands for running tests and generating coverage reports:

*   **Run all tests:**
    ```bash
    poetry run pytest
    ```
    Executes the entire test suite.

*   **Run tests with coverage:**
    ```bash
    poetry run pytest --cov
    ```
    Runs all tests and collects code coverage information.

*   **Generate an HTML coverage report:**
    ```bash
    poetry run pytest --cov --cov-report=html
    ```
    Generates a detailed HTML report of code coverage, which can be found in the `htmlcov/` directory. This report helps identify untested parts of the codebase.

## Database Seeding

The template includes a powerful management command to populate your database with sample data, which is invaluable for development and testing. This command is part of the `apps/core/management/commands/seed.py` module.

**Usage:**

```bash
# Basic seeding with default options (creates 10 users)
poetry run seed

# Create a specific number of users
poetry run seed --users 20

# Create a superuser (admin@admin.com:admin)
poetry run seed --superuser

# Clean existing data before seeding
poetry run seed --clean

# Combine options
poetry run seed --users 50 --superuser --clean
```

**Options:**

*   `--users <number>`: Specifies the number of regular users to create. Default is 10.
*   `--superuser`: Creates a default superuser (`admin@admin.com` with password `admin`).
*   `--clean`: Cleans (deletes) existing seeded data before generating new data. Use with caution as this will remove all existing users and related data.

## Asynchronous Tasks (Celery)

For handling background tasks and asynchronous operations, the project integrates Celery. To run Celery workers and schedulers, use the following commands:

*   **Start the Celery worker:**
    ```bash
    poetry run worker
    ```
    This command starts a Celery worker process that executes tasks from the message queue.

*   **Start the Celery beat scheduler:**
    ```bash
    poetry run beat
    ```
    This command starts the Celery beat scheduler, which is responsible for periodically executing scheduled tasks.

## Environment Variables

Environment variables are managed using a `.env` file, which is crucial for configuring application settings without hardcoding sensitive information. The project uses `django-environ` to load these variables.

*   **Development `.env` file:** The `poetry run create_dev_env` command can be used to generate a new `.env` file tailored for development purposes if it's missing or needs to be reset.
*   **Production `.env` file:** For production deployments, refer to the `.env.example` file at the project root for a comprehensive list of all required environment variables and their descriptions. This file serves as a template for setting up your production environment.
