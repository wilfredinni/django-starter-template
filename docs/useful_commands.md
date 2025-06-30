# Useful Commands

This section provides a consolidated list of useful commands to help you manage and develop your Django project efficiently. These commands cover various aspects, including running the development server, managing migrations, executing tests, handling Celery tasks, and seeding the database.

## General Development Commands

*   **Start the Development Server:**

    ```bash
    poetry run server
    ```
    Alternatively:
    ```bash
    python manage.py runserver
    ```

    Starts the Django development server, typically accessible at `http://127.0.0.1:8000/`.

*   **Make Migrations:**

    ```bash
    poetry run makemigrations
    ```
    Alternatively:
    ```bash
    python manage.py makemigrations
    ```

    Creates new database migrations based on changes detected in your models.

*   **Apply Migrations:**

    ```bash
    poetry run migrate
    ```
    Alternatively:
    ```bash
    python manage.py migrate
    ```

    Applies pending database migrations, updating your database schema.

*   **Create a Superuser:**

    ```bash
    python manage.py createsuperuser
    ```

    Creates an administrative user for the Django admin panel.

*   **Create Development Environment File:**

    ```bash
    poetry run create_dev_env
    ```

    Generates a `.env` file with basic development settings. This is particularly useful when setting up the project for the first time outside of a Dev Container.

## Celery Task Management

*   **Start Celery Worker:**

    ```bash
    poetry run worker
    ```

    Starts a Celery worker process to execute asynchronous tasks. This command should be run in a separate terminal or as a background process.

*   **Start Celery Beat (Scheduler):**

    ```bash
    poetry run beat
    ```

    Starts the Celery Beat scheduler, which is responsible for kicking off periodic tasks defined in the Django admin.

## Testing Commands

*   **Run All Tests:**

    ```bash
    poetry run pytest
    ```

    Executes all discovered tests in your project.

*   **Run Tests with Code Coverage:**

    ```bash
    poetry run pytest --cov
    ```

    Runs tests and generates a summary of code coverage in the terminal.

*   **Generate HTML Coverage Report:**

    ```bash
    poetry run pytest --cov --cov-report=html
    ```

    Runs tests and generates a detailed HTML report of code coverage, which can be viewed in your web browser.

## Database Seeding Commands

*   **Seed Database with Default Users (10 users):**

    ```bash
    poetry run seed
    ```
    Alternatively:
    ```bash
    python manage.py seed
    ```

    Populates the database with a default number of fake users.

*   **Seed Database with a Specific Number of Users:**

    ```bash
    poetry run seed --users <count>
    ```

    Creates a specified number of fake users.

*   **Create a Superuser during Seeding:**

    ```bash
    poetry run seed --superuser
    ```

    Creates an administrative user (`admin@admin.com` with password `admin`) along with other seeded data.

*   **Clean Database Before Seeding:**

    ```bash
    poetry run seed --clean
    ```

    Deletes all existing non-superuser user data before populating the database with new data.

*   **Combine Seeding Options:**

    ```bash
    poetry run seed --users 50 --superuser --clean
    ```

    You can combine multiple options to customize the seeding process.
