# Gemini CLI Agent

This page provides specific guidelines and context for the Gemini CLI agent when interacting with the `django-starter-template` project. For the full, up-to-date guidelines, please refer to the `GEMINI.md` file in the project root.

## Project Overview

This project is a Django REST Framework API template designed for rapid development. It includes pre-configured setups for authentication, background tasks, API documentation, and structured logging.

## Key Technologies and Conventions

*   **Framework**: Django 5.x
*   **API Framework**: Django REST Framework (DRF)
*   **Dependency Management**: [Poetry](https://python-poetry.org/)
    *   Always use `poetry run <command>` for executing project-specific scripts or commands (e.g., `poetry run server`, `poetry run pytest`).
    *   Dependencies are defined in `pyproject.toml` and managed by `poetry.lock`.
*   **Testing**: [Pytest](https://docs.pytest.org/en/stable/)
    *   Test files are typically located in `apps/<app_name>/tests/`.
    *   Run tests using `poetry run test` or `poetry run pytest`.
    *   Code coverage can be generated with `poetry run test-cov`.
*   **API Documentation**: [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
    *   OpenAPI 3 schema generation.
    *   Schema definitions are often centralized in `schema.py` files within apps (e.g., `apps/users/schema.py`).
    *   Use `@extend_schema` decorator for detailed API documentation.
*   **Documentation (MkDocs)**: [MkDocs](https://www.mkdocs.org/) with Material theme.
    *   Documentation source files are in the `docs/` directory.
    *   The `mkdocs.yml` file configures the documentation site.
    *   When refactoring documentation, maintain the style and structure observed in `logging.md`, `tasks.md`, `rate_limiting.md`, `database_seeding.md`, `testing.md`, `environment_setup.md`, and `copilot_prompts.md`.
*   **Environment Variables**: Managed using `django-environ`.
    *   Configuration is loaded from `.env` files. Refer to `.env.example` for required variables.
*   **Asynchronous Tasks**: [Celery](https://docs.celeryq.dev/en/stable/) with Redis as broker and backend.
    *   Celery worker: `poetry run worker`
    *   Celery beat scheduler: `poetry run beat`
*   **Logging**: Structured JSON logging.
    *   Logs are typically written to the `logs/` directory.
    *   Request tracing is implemented via `RequestIDMiddleware`.
*   **Code Quality**: [Flake8](https://flake8.pycqa.org/en/latest/) for linting.
    *   Configuration is in `.flake8`.
*   **Development Environment**: Designed for use with VS Code Dev Containers.
    *   Ensures a consistent and reproducible development setup.

## General Instructions for Gemini

*   **Adhere to existing code style**: When modifying or adding code, always match the surrounding code's formatting, naming conventions, and architectural patterns.
*   **Verify dependencies**: Before suggesting or implementing new libraries, check `pyproject.toml` and `poetry.lock` to see if they are already in use. If not, propose adding them via Poetry.
*   **Prioritize existing solutions**: Leverage existing project features (e.g., `drf-spectacular` for API docs, Celery for background tasks) before introducing new tools or patterns.
*   **Explain shell commands**: For any `run_shell_command` that modifies the file system or project state, provide a brief explanation of its purpose and potential impact.
*   **Testing**: If a change involves logic, consider if new or updated tests are appropriate. Use `poetry run test` to verify changes.
*   **Documentation**: If new features or significant changes are introduced, update the relevant documentation in the `docs/` directory, following the established style.
