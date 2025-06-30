# Project Structure

Understanding the project's directory structure is key to navigating and contributing to the Django Starter Template. This document provides a detailed overview of the main directories and files, explaining their purpose and contents.

```
├── .devcontainer/              # Dev container configuration
├── .github/                    # GitHub CI/CD workflows and issue templates
├── .vscode/                    # VS Code settings and recommended extensions
├── apps/                       # Django applications (core logic)
│   ├── core/                   # Core functionalities and shared components
│   │   ├── management/         # Custom Django management commands
│   │   ├── tests/              # Unit and integration tests for core app
│   │   ├── schema.py           # OpenAPI schema definitions for core app
│   │   ├── tasks.py            # Celery task definitions for core app
│   │
│   └── users/                  # User management and authentication app
│       ├── tests/              # Unit and integration tests for users app
│       ├── managers.py         # Custom managers for user models
│       ├── models.py           # User model definition
│       ├── schema.py           # OpenAPI schema definitions for users app
│       ├── throttles.py        # Rate limiting configurations for user-related views
│       ├── views.py            # API views for user authentication and profile management
│
├── conf/                       # Project-wide configuration
│   ├── settings.py             # Main Django settings file
│   ├── test_settings.py        # Settings specifically for running tests
│   ├── celery.py               # Celery application configuration
│   ├── urls.py                 # Main URL routing for the project
│   ├── wsgi.py                 # WSGI application entry point
│
├── logs/                       # Application log files
├── scripts/                    # Utility scripts for various development tasks
├── static/                     # Static files (CSS, JavaScript, images)
├── templates/                  # Project-wide HTML templates
├── .env.example                # Example environment variables file
├── .flake8                     # Flake8 linter configuration
├── .gitignore                  # Git ignore file
├── manage.py                   # Django's command-line utility
├── notebook.ipynb              # Jupyter Notebook for interactive development
├── pyproject.toml              # Project dependencies and metadata (Poetry)
├── pytest.ini                  # Pytest configuration
├── README.md                   # Project README file
├── renovate.json               # Renovate Bot configuration for dependency updates
├── SECURITY.md                 # Security policy and guidelines
```

## Key Directories and Their Purpose

*   **`.devcontainer/`**: Contains configuration files for Visual Studio Code Dev Containers. This ensures a consistent and reproducible development environment across different machines.

*   **`.github/`**: Stores GitHub-specific files, including GitHub Actions workflows for Continuous Integration (CI), issue templates, and other repository settings.

*   **`.vscode/`**: Holds Visual Studio Code workspace settings and recommended extensions for the project, enhancing the development experience.

*   **`apps/`**: This is the core of your Django project, where individual Django applications reside. Each app is a self-contained module responsible for a specific feature or set of features.
    *   **`core/`**: Houses fundamental functionalities and shared components that are used across different parts of the application. This includes custom management commands, base Celery tasks, and common API schema definitions.
    *   **`users/`**: Manages all aspects of user authentication and authorization, including user models, serializers, views, and related utilities.

*   **`conf/`**: Contains project-wide configuration files that apply to the entire Django project, rather than a specific app. This includes the main `settings.py`, URL routing, WSGI configuration, and Celery setup.

*   **`logs/`**: The designated directory for application log files. Different log levels and types (e.g., general, security, error) are typically written to separate files within this directory.

*   **`scripts/`**: A collection of utility scripts that automate various development and maintenance tasks, such as running the server, migrations, or custom commands.

*   **`static/`**: Stores static assets like CSS, JavaScript, and images that are served directly by the web server.

*   **`templates/`**: Contains project-wide HTML templates that are not specific to any single Django application.

## Key Files and Their Purpose

*   **`.env.example`**: A template file that outlines all the environment variables required by the project. Developers should copy this to `.env` and fill in their specific values.

*   **`manage.py`**: Django's command-line utility for administrative tasks. You'll use this for running the development server, migrations, and custom management commands.

*   **`pyproject.toml`**: Used by Poetry (the dependency management tool) to define project metadata, dependencies, and build configurations.

*   **`pytest.ini`**: Configuration file for `pytest`, specifying how tests should be discovered and run, including settings for code coverage.

*   **`README.md`**: The main project documentation, providing a high-level overview, quick start instructions, and key features.

By adhering to this structured layout, the project promotes modularity, maintainability, and scalability, making it easier for developers to understand and contribute to the codebase.
