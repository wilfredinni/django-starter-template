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


## Todo

- [x] Index Page with a link to the Django admin
- [x] OpenAPI 3 schema generation and Swagger
- [x] CI with Github Actions
- [x] Add a restore method for soft deleted data
- [ ] Data seeding
- [ ] Production Docker file
- [ ] Production Docker compose file
- [ ] CD with Github Actions
