<div align="center">
    <img src="https://raw.githubusercontent.com/wilfredinni/django-starter-template/refs/heads/main/static/logo.png" data-canonical-src="/logo.png" width="130" height="130" />

# Django starter template

A comprehensive and easy-to-use starting point for your new API with **Django** and **DRF**.

[![Test Status](https://github.com/wilfredinni/django-starter-template/actions/workflows/test.yml/badge.svg)](https://github.com/wilfredinni/django-starter-template/actions/workflows/test.yml)
[![CodeQL Status](https://github.com/wilfredinni/django-starter-template/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/wilfredinni/django-starter-template/actions/workflows/github-code-scanning/codeql)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/wilfredinni/django-starter-template?tab=MIT-1-ov-file#readme)
</div>


## ✨ Key Features

This template is packed with features to help you build amazing APIs:

-   **User Authentication:** Secure token-based authentication with `django-rest-knox`.
-   **Background Tasks:** Asynchronous task processing with `Celery` and `Redis`.
-   **API Documentation:** Automatic OpenAPI 3 schema generation with `drf-spectacular`.
-   **Centralized Logging:** Structured JSON logging for easy monitoring.
-   **Custom User Model:** Email-based authentication for a modern user experience.
-   **And much more!** Explore the documentation to discover all the features.

## Quick Start

### Prerequisites
- 💻 VS Code
- 🐋 Docker
- 🐳 Docker Compose

### Setup Steps
1. Use [GitHub's template feature](https://github.com/new?template_name=django-starter-template&template_owner=wilfredinni) (recommended) or clone repository
2. Open in VS Code
3. Check [Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree) in the sidebar for setup guidance
4. Run `CTL/CMD + Shift + p` and select `Reopen in container`
5. Create superuser: `python manage.py createsuperuser`
6. Start server: `python manage.py runserver`

## 📖 Explore the Documentation

This documentation is your guide to building amazing applications with the Django Starter Template. Use the navigation on the left to explore the different sections.

-   **[Development](development.md):** Learn about the development workflow, including how to run tests, and use the scripts.
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