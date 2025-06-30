# Welcome to the Django Starter Template!

<p align="center">
  <img src="assets/logo.png" alt="Django Starter Template Logo" width="200"/>
</p>

<p align="center">
  <strong>A comprehensive starting point for your new API with Django and DRF.</strong>
</p>

---

## 🚀 Quick Start

The recommended way to get started is by using the Dev Container feature in VS Code.

### Prerequisites
- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code.

### Setup Steps

1.  **Use the GitHub Template:**
    - Click the green `Use this template` button on the [GitHub repository page](https://github.com/wilfredinni/django-starter-template) to create your own repository.

2.  **Open in VS Code:**
    - Clone your new repository and open its folder in Visual Studio Code.

3.  **Check the Setup Guide:**
    - Before proceeding, check the **`Todo Tree`** view in the VS Code sidebar for a guided list of initial setup tasks.

4.  **Reopen in Container:**
    - When prompted, click **"Reopen in Container"** to build and start the dev environment.

5.  **Create a Superuser:**
    - Once the container is running, open a new VS Code terminal (`Ctrl+` or `Terminal > New Terminal`).
    - Run the following command:
    ```bash
    python manage.py createsuperuser
    ```

6.  **Start the Server:**
    - In the same terminal, run:
    ```bash
    python manage.py runserver
    ```

Your API is now running and accessible at `http://127.0.0.1:8000`.

3.  **Set up your environment:**

    ```bash
    cp .env.example .env
    # Edit .env with your settings
    ```

4.  **Install dependencies and run migrations:**

    ```bash
    poetry install
    poetry run migrate
    ```

5.  **Launch the development server:**

    ```bash
    poetry run server
    ```

That's it! Your new Django project is live at `http://127.0.0.1:8000`.

---

## ✨ Key Features

This template is packed with features to help you build amazing APIs:

-   **User Authentication:** Secure token-based authentication with `django-rest-knox`.
-   **Background Tasks:** Asynchronous task processing with `Celery` and `Redis`.
-   **API Documentation:** Automatic OpenAPI 3 schema generation with `drf-spectacular`.
-   **Centralized Logging:** Structured JSON logging for easy monitoring.
-   **Custom User Model:** Email-based authentication for a modern user experience.
-   **And much more!** Explore the documentation to discover all the features.

---

## 📖 Explore the Documentation

This documentation is your guide to building amazing applications with the Django Starter Template. Use the navigation on the left to explore the different sections.

-   **[Development](development.md):** Learn about the development workflow, including how to run tests, and use the provided scripts.
-   **[Project Structure](project_structure.md):** Get an overview of the project's directory structure.
-   **[Project Settings](settings.md):** Understand the available settings and how to configure your project.
-   **[Dependencies](dependencies.md):** See a list of all the project's dependencies.
-   **[Authentication](authentication.md):** Learn how to use the authentication and user management endpoints.
-   **[Core App](core_endpoints.md):** Discover the core functionalities and API endpoints.
-   **[Logging](logging.md):** Understand the logging system and how to use it.
-   **[Celery Tasks](tasks.md):** Learn how to create and manage background tasks.
-   **[Rate Limiting](rate_limiting.md):** Configure rate limiting to protect your API.
-   **[Database Seeding](database_seeding.md):** Learn how to seed your database with initial data.
-   **[Testing](testing.md):** Understand how to run and write tests for your project.
-   **[Environment Setup](environment_setup.md):** Learn how to set up your development environment.
-   **[Useful Commands](useful_commands.md):** A list of useful commands for development.
