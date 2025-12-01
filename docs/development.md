# Development Workflow

## Overview

This guide outlines the essential commands and best practices for developing your application within the Django Starter Template. You can choose between two development approaches:

1. **Dev Container** (recommended for beginners) - Everything runs in a container with VS Code attached
2. **Docker Compose** (recommended for standard development) - Services run in containers, you work on your local machine

## Development Setup Options

### Option 1: Docker Compose (Recommended)

This approach runs all services (PostgreSQL, Redis, Django, Celery) in Docker containers while you work on your local machine with full IDE support.

**1. (Optional) Create `.env` file:**

Docker Compose already defines environment variables, but if you need a local `.env` file:

```bash
cp .env.example .env
```

**2. Start services:**
```bash
docker compose up
```

This starts:
- `db` - PostgreSQL database on port 5432
- `redis` - Redis cache on port 6379
- `backend` - Django development server on port 8000
- `worker` - Celery worker for background tasks
- `beat` - Celery beat scheduler

**3. Enable IDE support (IntelliSense, autocomplete):**

For VS Code to recognize dependencies, install them locally:

```bash
poetry install
```

This creates a local virtual environment that VS Code uses for:
- Code completion and IntelliSense
- Import resolution
- Type checking
- Linting and formatting

**Note:** Your code still runs in Docker containers, but VS Code uses the local environment for editor features.

**4. Common tasks:**

```bash
# Run migrations in the backend container
docker compose exec backend python manage.py migrate

# Create migrations
docker compose exec backend python manage.py makemigrations

# Create superuser
docker compose exec backend python manage.py createsuperuser

# Run Django shell
docker compose exec backend python manage.py shell

# View logs
docker compose logs -f backend

# Rebuild containers after dependency changes
docker compose up --build

# Stop all services
docker compose down
```

**Important:** If your `.env` file contains special characters like `$` in values (e.g., in `DJANGO_SECRET_KEY`), escape them with `$$` to prevent Docker Compose from treating them as variables:

```ini
# Bad - Docker Compose interprets $d as a variable
DJANGO_SECRET_KEY=secret-key-with-$d-in-it

# Good - Escaped with $$
DJANGO_SECRET_KEY=secret-key-with-$$d-in-it
```

### Option 2: Dev Container

This approach runs VS Code itself inside a container.

**Setup:**
1. Open VS Code
2. Press `Ctrl/Cmd + Shift + P`
3. Select "Dev Containers: Reopen in Container"
4. Wait for the container to build and VS Code to reload

**Advantages:**
- Everything is containerized
- Consistent environment across all developers
- No local Python installation needed

**Disadvantages:**
- Slower file system performance on macOS/Windows
- More resource intensive
- Less flexible for running multiple projects

## Core Development Commands

When working locally (with Docker Compose) or inside the Dev Container, use these `poetry run` commands:

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

For handling background tasks and asynchronous operations, the project integrates Celery.

**With Docker Compose:**
Celery worker and beat are automatically started as separate services. Check their logs:
```bash
docker compose logs -f worker
docker compose logs -f beat
```

**With Dev Container or local Poetry:**

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
