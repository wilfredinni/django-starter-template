<div align="center">
    <img src="https://raw.githubusercontent.com/wilfredinni/django-starter-template/refs/heads/main/static/logo.png" data-canonical-src="/logo.png" width="130" height="130" />

# Django starter template

A comprehensive and easy-to-use starting point for your new API with **Django** and **DRF**.

[![Test Status](https://github.com/wilfredinni/django-starter-template/actions/workflows/test.yml/badge.svg)](https://github.com/wilfredinni/django-starter-template/actions/workflows/test.yml)
[![CodeQL Status](https://github.com/wilfredinni/django-starter-template/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/wilfredinni/django-starter-template/actions/workflows/github-code-scanning/codeql)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/wilfredinni/django-starter-template?tab=MIT-1-ov-file#readme)
</div>

## Key features

This template includes battle-tested features for building secure, scalable, and maintainable APIs

### Core Features
- 🚀 Latest [Django](https://docs.djangoproject.com/en/5.1/) (5+) with full feature set
- 🛠️ [Django Rest Framework](https://www.django-rest-framework.org/) for API development
- 📖 API documentation with [drf-spectacular](https://drf-spectacular.readthedocs.io/) and [Swagger](https://swagger.io/)

### Database & Caching
- 💿 Pre-configured [PostgreSQL](https://www.postgresql.org/) database
- 📦 [Redis](https://redis.io/) caching system
- 🗄️ BaseModel with `created_at` and `updated_at` fields
- 🗑️ Optional SoftDeleteBaseModel for soft deletions

### Authentication & Users
- 🔒 Complete auth system using [Knox](https://jazzband.github.io/django-rest-knox/)
- 🙋 Extended user model with email-based authentication

### Task Management
- ⏳ [Celery](https://docs.celeryq.dev/en/stable/) for async tasks with BaseTaskWithRetry
- 🗃️ Task results storage with django_celery_results
- 📅 Task scheduling through django_celery_beat

### Development Tools
- 🧪 Testing with [Pytest](https://docs.pytest.org/en/stable/)
- ⚡ Interactive development using Jupyter Notebooks
- 🐞 Debugging with Django Debug Toolbar
- 🔧 Code quality tools: [Black](https://black.readthedocs.io/), [Flake8](https://flake8.pycqa.org/)
- 👨‍💻 [VS Code](https://code.visualstudio.com/) with [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

### Additional Features
- 🔽 Advanced filtering with django-filter
- 🧩 Extended functionality with Django Extensions


## Requirements

- 💻 VS Code
- 🐋 Docker
- 🐳 Docker Compose


## How to use

1. Use [GitHub's template feature](https://github.com/new?template_name=django-starter-template&template_owner=wilfredinni) (recommended) or clone repository and delete the `.git` folder.
1. Open the project in VS Code.
1. If you installed the recommended extensions, open `Todo Tree` in the sidebar. It will [guide you trough the first steps](/static/TODO.png) setting up your project, like changing the name of the container, adjusting your URLS, etc.
1. Hit `CTL/CMD + Shift + p` and select `Reopen in container`. This will:
    - Create a dev container.
    - Setup a Redis server.
    - Setup your PostgreSQL database.
    - Add a development `.env` file.
    - Install the dependencies.
    - Migrate the database.
1. Create your super user with `python manage.py createsuperuser`.
1. Run the project with `python manage.py reserver`.
1. Work as usual.

## Project Structure

```
├── apps/
│   ├── core/                   # Core functionality
│   │   ├── management/         # Custom management commands
│   │   │   └── commands/
│   │   │       └── seed.py     # Database seeding utility
│   │   ├── tests/              # Core app tests
│   │   ├── models.py           # Base models and abstractions
│   │   ├── managers.py         # Custom model managers
│   │   ├── schema.py           # API schema definitions
│   │   ├── tasks.py            # Celery tasks
│   │
│   └── users/                  # User management app
│       ├── tests/              # User app tests
│       ├── admin.py            # Admin interface customization
│       ├── forms.py            # User-related forms
│       ├── managers.py         # User model managers
│       ├── models.py           # User model definition
│       ├── schema.py           # User API schemas
│       ├── throttles.py        # Rate limiting
│
├── conf/                       # Project configuration
│   ├── settings.py             # Main settings file
│   ├── test_settings.py        # Test-specific settings
│   ├── celery.py               # Celery configuration
│
├── logs/                       # Application logs
│
├── scripts/                    # Utility scripts
│   ├── bump.py                 # Version management
│   ├── celery.py               # Celery commands
│   └── django.py               # Django commands
│
├── templates/
│   ├── 404.html                # 404 Error page
│   ├── 500.html                # 500 Error pages
│   └── index.html              # Main template
│
├── .devcontainer/              # Dev container config
│
├── .github/
│   └── workflows/              # CI/CD workflows
│
├── pyproject.toml              # Project dependencies
├── pytest.ini                  # Testing configuration
```

## Models

### BaseModel

All models in the project can inherit from `BaseModel` which provides:

- `created_at`: Timestamp of record creation
- `updated_at`: Timestamp of last update

```python
class MyModel(BaseModel):
    name = models.CharField(max_length=255)
```

### SoftDeleteBaseModel

Extends `BaseModel` with soft deletion capability:
- `deleted_at`: Timestamp of soft deletion
- Includes `restore()` method to undelete records
- Custom manager that filters out deleted records by default

```python
class MyModel(SoftDeleteBaseModel):
    name = models.CharField(max_length=255)
```

## Authentication

The template uses Knox for token-based authentication:

### Available Endpoints

- `POST /auth/create/` - Create a new user
- `POST /auth/login/` - Log in and receive token
- `POST /auth/logout/` - Invalidate current token
- `POST /auth/logoutall/` - Invalidate all tokens
- `GET/PUT/PATCH /auth/profile/` - Manage user profile

### Rate Limiting

- Login attempts: 5 per minute
- User operations: 1000 per day
- Anonymous operations: 100 per day

## Advanced Usage

### Celery Tasks

Base task class with retry capabilities:

```python
from apps.core.tasks import BaseTaskWithRetry

@shared_task(base=BaseTaskWithRetry)
def my_task():
    # Will retry 3 times with exponential backoff
    pass
```

### Environment Variables

The template supports multiple environment configurations:

- Development: `.env` file created automatically
- Production: See `.env.example` for required variables

### Testing

- Tests are organized by app in `tests/` directories
- Uses pytest fixtures for common testing scenarios
- Includes comprehensive test coverage for authentication
- Includes examples of API endpoint testing

### API Documentation

- Swagger UI available at `/api/schema/swagger-ui/`
- Automatic schema generation with drf-spectacular
- Includes example requests and responses
- Documents authentication requirements

### Security Features

- Email-based authentication
- Token-based authorization
- Rate limiting and throttling
- CORS configuration
- Debug mode control
- Secure password hashing

## Development Best Practices

1. **Model Creation**
   - Inherit from `BaseModel` for basic timestamping
   - Use `SoftDeleteBaseModel` when deletion tracking is needed
   - Implement custom managers in `managers.py` in each app

2. **API Views**
   - Use DRF class-based views
   - Implement proper authentication
   - Add rate limiting
   - Document with drf-spectacular decorators

3. **Testing**
   - Write tests for all models and views
   - Use pytest fixtures
   - Test both success and failure cases
   - Test authentication and permissions

4. **Task Processing**
   - Use `BaseTaskWithRetry` for resilient tasks
   - Configure retry policies appropriately
   - Use Celery Beat for scheduled tasks

## Commands 🛠️

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

## Todo

- [x] Index Page with a link to the Django admin
- [x] OpenAPI 3 schema generation and Swagger
- [x] CI with Github Actions
- [x] Add a restore method for soft deleted data
- [x] Data seeding
- [ ] Production Docker file
- [ ] Production Docker compose file
- [ ] CD with Github Actions
