<h1 align="center">Welcome to the Django Starter Template!</h1>

<p align="center">
  <img src="assets/logo.png" alt="Django Starter Template Logo" width="150"/>
</p>

<p align="center">
  <strong>A comprehensive starting point for your new API with Django and DRF.</strong>
</p>

## Overview

This documentation provides a comprehensive guide to the Django Starter Template, a robust foundation for building modern APIs with Django and Django REST Framework. It covers everything from initial setup and development workflows to advanced features like authentication, background tasks, and automated documentation.

## Quick Start

The recommended way to get started is by using the Dev Container feature in VS Code.

### Prerequisites

To get started with the Dev Container, ensure you have the following installed:

*   [Visual Studio Code](https://code.visualstudio.com/)
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/)
*   [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code

### Setup Steps

Follow these steps to set up your development environment using the Dev Container:

1.  **Use the GitHub Template:** Begin by creating your own repository from the [Django Starter Template GitHub page](https://github.com/wilfredinni/django-starter-template) by clicking the green `Use this template` button.

2.  **Open in VS Code:** Clone your newly created repository to your local machine and open the project folder in Visual Studio Code.

3.  **Check the Setup Guide:** Before proceeding, consult the **`Todo Tree`** view in the VS Code sidebar. This provides a guided checklist of initial setup tasks to ensure a smooth start.

4.  **Reopen in Container:** Upon opening the project, VS Code will prompt you to "Reopen in Container." Click this option to build and launch the development environment. This process automatically configures essential services like Redis, Celery, and PostgreSQL, installs all project dependencies, and applies database migrations.

5.  **Create a Superuser:** Once the container is ready, create an administrative user for accessing the Django admin interface by running: `python manage.py createsuperuser`.

6.  **Start the Server:** Launch the Django development server with: `python manage.py runserver`.

Your API should now be running and accessible at `http://127.0.0.1:8000`.

## Key Features

This template comes equipped with a rich set of features designed to accelerate your API development:

*   **User Authentication:** Implements secure, token-based authentication using `django-rest-knox`, providing a robust system for user management and access control.
*   **Background Tasks:** Leverages `Celery` and `Redis` for efficient asynchronous task processing, enabling your application to handle long-running operations without blocking the main thread.
*   **API Documentation:** Features automatic OpenAPI 3 schema generation with `drf-spectacular`, ensuring your API documentation is always up-to-date and easily explorable via Swagger UI.
*   **Centralized Logging:** Provides a structured JSON logging system for comprehensive and easily parsable application logs, facilitating monitoring and debugging.
*   **Custom User Model:** Utilizes a custom user model with email-based authentication, offering flexibility and a modern approach to user identity.
*   **GitHub Copilot Prompts:** Includes a collection of useful prompts tailored to enhance your development experience with GitHub Copilot, boosting productivity.
*   **Comprehensive Documentation:** This documentation serves as a detailed guide to all features and functionalities, helping you maximize the template's potential.

---

## Explore the Documentation

This documentation is your comprehensive guide to building robust applications with the Django Starter Template. Use the navigation on the left to explore various aspects of the project:

*   **[Development](development.md):** Learn about the development workflow, including how to run tests, and utilize provided scripts.
*   **[Project Structure](project_structure.md):** Gain an overview of the project's directory structure and organization.
*   **[Project Settings](settings.md):** Understand the available settings and how to configure your project for different environments.
*   **[Dependencies](dependencies.md):** Review a detailed list of all the project's dependencies and their purposes.
*   **[Authentication](authentication.md):** Dive into the authentication system, covering user management and API endpoints.
*   **[Core Application](core_endpoints.md):** Discover the core functionalities and essential API endpoints provided by the `apps/core` application.
*   **[Logging](logging.md):** Understand the structured logging system and how to effectively use it for monitoring and debugging.
*   **[Celery Tasks](tasks.md):** Learn how to create, manage, and monitor background tasks using Celery.
*   **[Rate Limiting](rate_limiting.md):** Configure and understand rate limiting to protect your API from abuse and ensure fair usage.
*   **[Database Seeding](database_seeding.md):** Learn how to populate your database with initial data for development and testing.
*   **[Testing](testing.md):** Understand how to write and run tests for your project to ensure code quality and reliability.
*   **[Environment Setup](environment_setup.md):** Get detailed instructions on setting up your development environment.
*   **[AI Tools](ai_tools):** Explore useful prompts to enhance your development experience with GitHub Copilot, Gemini CLI agent, and Roo Code.
