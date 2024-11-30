<div align="center">
    <img src="https://raw.githubusercontent.com/wilfredinni/django-starter-template/refs/heads/main/static/logo.png" data-canonical-src="/logo.png" width="130" height="130" />

# Django starter template

A comprehensive and easy-to-use starting point for your new API with **Django** and **DRF**.

[![Test Status](https://github.com/wilfredinni/django-starter-template/actions/workflows/test.yml/badge.svg)](https://github.com/wilfredinni/django-starter-template/actions/workflows/test.yml)
[![CodeQL Status](https://github.com/wilfredinni/django-starter-template/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/wilfredinni/django-starter-template/actions/workflows/github-code-scanning/codeql)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/wilfredinni/django-starter-template?tab=MIT-1-ov-file#readme)
</div>

## Key features

- 🧪 Fully tested with [Pytest](https://docs.pytest.org/en/stable/).
- 🚀 Enjoy the latest version of [Django](https://docs.djangoproject.com/en/5.1/) (5+) with all its features and improvements.
- 🛠️ [Django Rest Framework](https://www.django-rest-framework.org/) for building APIs.
- 💿 Start your project with [PostgreSQL](https://www.postgresql.org/) without the need to install and configure it.
- 📦 [Redis](https://redis.io/) caching out of the box.
- 🔒 Login, Logout, Logout all, User profile and creation with [Knox](https://jazzband.github.io/django-rest-knox/), an easy-to-use authentication for DRF.
- 🙋 Extended user model and a custom manager. Start with the email as the unique identifier.
- 🗄️ A custom [BaseModel](/apps/core/models.py) to easily add `created_at` and `updated_at` fields to your models.
- 🗑️ A custom [SoftDeleteBaseModel](/apps/core/models.py) to add soft delete functionality to the models you choose to.
- ⏳ Fully configured asynchronous tasks with [Celery](https://docs.celeryq.dev/en/stable/). It also includes a reusable [BaseTaskWithRetry](/apps/core/tasks.py).
- 🗃️ [django_celery_results](https://django-celery-results.readthedocs.io/en/latest/) enables Celery to store task results using Django's database backend.
- 📅 [django_celery_beat](https://django-celery-beat.readthedocs.io/en/latest/) for periodic task scheduling using the Django admin interface.
- 🔽 [django-filter](https://django-filter.readthedocs.io/en/stable/) add support for complex filtering of querysets in Django and DRF views.
- 📖 Auto document your API with [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html) and [Swagger](https://swagger.io/).
- ⚡[Test your queries and code](/notebook.ipynb) interactively with [Jupyter Notebooks](https://jupyter.org/).
- 🐞 [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) for debugging and profiling.
- 🧩 [Django Extensions](https://django-extensions.readthedocs.io/en/latest/) for custom management commands and model enhancements.
- 🔧 Get out of the box code formatting with [Black](https://black.readthedocs.io/en/stable/), linting with [Flake8](https://flake8.pycqa.org/en/latest/) and test with [Pytest](https://docs.pytest.org/en/stable/).
- 👨‍💻 Develop with [VS Code](https://code.visualstudio.com/) and [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers).


## Requirements

- 💻 VS Code
- 🐋 Docker
- 🐳 Docker Compose


## How to use

1. [Create a new project with this template](https://github.com/new?template_name=django-starter-template&template_owner=wilfredinni) (recommended) or clone the repository and delete the `.git` folder.
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


## Commands

This template comes with some shortcuts so you don't have to memorize how to start the workers:

- `poetry run worker`: to start a new Celery worker.
- `poetry run beat`: to start your periodic tasks.

You can also use:

- `poetry run server` instead of `python manage.py runserver`
- `poetry run makemigrations` instead of `python manage.py makemigrations`
- `poetry run migrate` instead of `python manage.py migrate`
- `poetry run create_dev_env` to create a development `.env` file


## Todo

- [x] Index Page with a link to the Django admin
- [x] OpenAPI 3 schema generation and Swagger.
- [x] CI with Github Actions
- [ ] Add method to restore soft deleted data
- [ ] Email sending with celery
- [ ] Data seeding
- [ ] API Versioning
- [ ] Production Docker file
- [ ] Production Docker compose file
- [ ] CD with Github Actions
