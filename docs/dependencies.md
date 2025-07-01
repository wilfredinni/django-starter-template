# Project Dependencies

This project uses [Poetry](https://python-poetry.org/) to manage its dependencies. The main dependencies are listed in the `[tool.poetry.dependencies]` section of the `pyproject.toml` file, while development dependencies are in the `[tool.poetry.group.dev.dependencies]` section.

## Main Dependencies

- **python**: ^3.13
- **django**: ^5.1.2
- **django-environ**: ^0.12.0
- **django-cors-headers**: ^4.5.0
- **djangorestframework**: ^3.15.2
- **psycopg2**: ^2.9.10
- **whitenoise**: ^6.7.0
- **gunicorn**: ^23.0.0
- **django-rest-knox**: ^5.0.2
- **redis**: ^6.0.0
- **celery**: ^5.4.0
- **django-celery-beat**: ^2.7.0
- **django-celery-results**: ^2.5.1
- **sentry-sdk**: ^2.17.0 (with `django` extra)
- **django-redis**: ^6.0.0
- **drf-spectacular**: ^0.28.0
- **faker**: ^37.1.0
- **django-seed**: ^0.3.1
- **django-extensions**: ^4.1
- **django-filter**: ^25.1
- **python-json-logger**: ^3.3.0

## Development Dependencies

- **django-debug-toolbar**: ^5.0.0
- **pytest**: ^8.3.3
- **pytest-django**: ^4.9.0
- **ipykernel**: ^6.29.5
- **pytest-mock**: ^3.14.0
- **pytest-cov**: ^6.0.0
- **mkdocs**: ^1.6.0
- **mkdocs-material**: ^9.5.26
