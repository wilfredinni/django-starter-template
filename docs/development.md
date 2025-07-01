# Development Workflow

This guide covers the essential commands and practices for developing your application after you have completed the initial setup using the Dev Container.

## Core Development Commands

The project includes convenient scripts in `pyproject.toml` to simplify common development tasks. You should use these `poetry run` commands from the terminal inside your VS Code dev container.

| Command | Description |
| :--- | :--- |
| `poetry run server` | Starts the Django development server. |
| `poetry run makemigrations` | Creates new database migrations based on model changes. |
| `poetry run migrate` | Applies pending database migrations. |
| `poetry run test` | Runs the test suite using `pytest`. |
| `poetry run test-cov`| Runs the test suite and generates a coverage report. |

### Testing

The project uses `pytest` for testing.

- **Run all tests:**
  ```bash
  poetry run pytest
  ```
- **Run tests with coverage:**
  ```bash
  poetry run pytest --cov
  ```
- **Generate an HTML coverage report:**
  ```bash
  poetry run pytest --cov --cov-report=html
  ```
  The report will be generated in the `htmlcov/` directory.

## Database Seeding

The template includes a powerful seeding command to populate your database with sample data for development and testing.

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

## Asynchronous Tasks (Celery)

For handling background tasks, the project uses Celery.

- **Start the Celery worker:**
  ```bash
  poetry run worker
  ```
- **Start the Celery beat scheduler (for periodic tasks):**
  ```bash
  poetry run beat
  ```

## Environment Variables

- The project uses a `.env` file to manage environment variables.
- The `poetry run create_dev_env` command can be used to generate a new development `.env` file if needed.
- For production, refer to `.env.example` for the full list of required variables.
