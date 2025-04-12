<div align="center">
    <img src="https://raw.githubusercontent.com/wilfredinni/django-starter-template/refs/heads/main/static/logo.png" data-canonical-src="/logo.png" width="130" height="130" />

# Django starter template

A comprehensive and easy-to-use starting point for your new API with **Django** and **DRF**.

[![Test Status](https://github.com/wilfredinni/django-starter-template/actions/workflows/test.yml/badge.svg)](https://github.com/wilfredinni/django-starter-template/actions/workflows/test.yml)
[![CodeQL Status](https://github.com/wilfredinni/django-starter-template/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/wilfredinni/django-starter-template/actions/workflows/github-code-scanning/codeql)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/wilfredinni/django-starter-template?tab=MIT-1-ov-file#readme)
</div>

## Table of Contents
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Development Guide](#development-guide)
  - [Models](#models)
  - [Authentication](#authentication)
  - [API Documentation](#api-documentation)
  - [Testing](#testing)
  - [Task Processing](#task-processing)
    - [Tasks with retry](#tasks-with-retry)
    - [Scheduled Tasks](#scheduled-tasks)
- [Useful Commands](#useful-commands)
- [Environment Setup](#environment-setup)
- [Security Features](#security-features)
- [Project Structure](#project-structure)
- [Todo & Roadmap](#todo--roadmap)

## Key Features

### Core Platform
- 🚀 Django 5+ with full feature set
- 🛠️ Django Rest Framework for API development
- 📖 API documentation (drf-spectacular + Swagger)
- 💿 PostgreSQL database
- 📦 Redis caching
- ⏳ Celery task management

### Development Tools & Features
- 🧪 Pytest testing suite
- ⚡ Jupyter Notebooks integration
- 🐞 Django Debug Toolbar
- 🔧 Code quality tools (Black, Flake8)
- 👨‍💻 VS Code with Dev Containers
- 🔒 Knox authentication system
- 🔽 Advanced filtering capabilities

## Quick Start

### Prerequisites
- 💻 VS Code
- 🐋 Docker
- 🐳 Docker Compose

### Setup Steps
1. Use [GitHub's template feature](https://github.com/new?template_name=django-starter-template&template_owner=wilfredinni) (recommended) or clone repository
2. Open in VS Code
3. Check `Todo Tree` in the sidebar for setup guidance
4. Run `CTL/CMD + Shift + p` and select `Reopen in container`
5. Create superuser: `python manage.py createsuperuser`
6. Start server: `python manage.py runserver`

## Development Guide

### Authentication
The template uses Knox for token-based authentication:

#### Available Endpoints
- `POST /auth/create/` - Create a new user
- `POST /auth/login/` - Log in and receive token
- `POST /auth/logout/` - Invalidate current token
- `POST /auth/logoutall/` - Invalidate all tokens
- `GET/PUT/PATCH /auth/profile/` - Manage user profile

#### Rate Limiting
- Login attempts: 5 per minute
- User operations: 1000 per day
- Anonymous operations: 100 per day

### API Documentation
- Swagger UI available at `/api/schema/swagger-ui/`
- Automatic schema generation with drf-spectacular
- Includes example requests and responses
- Documents authentication requirements

### Testing
- Tests are organized by app in `tests/` directories
- Uses pytest fixtures for common testing scenarios
- Includes comprehensive test coverage for authentication
- Includes examples of API endpoint testing

### Task Processing

#### Tasks with retry
The template includes a base task class with retry capabilities. You can use it to create tasks that automatically retry on failure.

```python
from apps.core.tasks import BaseTaskWithRetry

@shared_task(base=BaseTaskWithRetry)
def my_task():
    # Will retry 3 times with exponential backoff
    pass
```

#### Scheduled Tasks
Scheduled tasks are managed with Celery Beat. You can define your periodic tasks in the `tasks.py` file of your app and configure them from the Django admin interface.

```python
from apps.core.tasks import BaseTask
@shared_task(base=BaseTask)
def my_periodic_task():
    # This task can be scheduled to run at regular intervals
    # from the Django admin interface
    pass
```

## Useful Commands
This section provides a list of useful commands to help you manage and develop your Django project efficiently.

### Celery Tasks
- `poetry run worker`: to start a new Celery worker.
- `poetry run beat`: to start your periodic tasks.

### Test commands:
- `pytest` to run the tests.
- `pytest --cov` to run the tests with coverage.
- `pytest --cov --cov-report=html` to run the tests with coverage and generate a HTML report.

### You can also use
- `poetry run server` instead of `python manage.py runserver`
- `poetry run makemigrations` instead of `python manage.py makemigrations`
- `poetry run migrate` instead of `python manage.py migrate`
- `poetry run create_dev_env` to create a development `.env` file
- `poetry run seed` to seed your database with sample data

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
- Development: `.env` file created automatically
- Production: See `.env.example` for required variables

## Security Features
- Email-based authentication
- Token-based authorization
- Rate limiting and throttling
- CORS configuration
- Debug mode control
- Secure password hashing

## Project Structure

```
├── .devcontainer/              # Dev container config
│
├── .github/                    # GitHub CI/CD workflows
│
├── .vscode/                    # VS Code settings
│
├── apps/
│   ├── core/                   # Core functionality
│   │   ├── management/         # Custom management commands
│   │   ├── tests/              # Core app tests
│   │   ├── schema.py           # API schema definitions
│   │   ├── tasks.py            # Celery base tasks
│   │
│   └── users/                  # User Management and Authentication app
│       ├── tests/              # User app tests
│       ├── managers.py         # User model managers
│       ├── models.py           # User model definition
│       ├── schema.py           # User API schemas
│       ├── throttles.py        # Rate limiting
│       ├── views.py            # User API views for authentication
│
├── conf/                       # Project configuration
│   ├── settings.py             # Main settings file
│   ├── test_settings.py        # Test-specific settings
│   ├── celery.py               # Celery configuration
│
├── logs/                       # Application Info and Error logs
│
├── scripts/                    # Utility scripts
│
├── .env.example                # Example environment variables
├── .flake8                     # Flake8 configuration
├── .gitignore                  # Git ignore file
├── manage.py                   # Django management script
├── notebook.ipynb              # Jupyter Notebook
├── pyproject.toml              # Project dependencies
├── pytest.ini                  # Testing configuration
```

## Todo & Roadmap
- [x] Index Page with a link to the Django admin
- [x] OpenAPI 3 schema generation and Swagger
- [x] CI with Github Actions
- [x] Data seeding
- [ ] Production Docker file
- [ ] Production Docker compose file
- [ ] CD with Github Actions
