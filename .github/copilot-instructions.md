# Django Starter Template - AI Development Guide

## Architecture Overview

This is a **production-ready Django 5.1+ API template** structured for scalability and maintainability.

- **Dependency Management**: Uses `uv` for ultra-fast package management (10-100x faster than pip/Poetry).
- **Authentication**: Custom email-based auth with `django-rest-knox`. No username field.
- **Async Tasks**: Celery + Redis with automatic retry patterns via `BaseTaskWithRetry`.
- **Logging**: Structured JSON logging (`python-json-logger`) with request ID tracking (`ContextVars`).
- **Documentation**: Auto-generated OpenAPI docs via `drf-spectacular`.

## Key Development Patterns

### 1. Project Structure
```
apps/                    # Django apps
├── users/               # Custom user model & auth
├── core/                # Shared utilities, middleware, tasks
conf/                    # Settings (django-environ)
scripts/                 # Ops scripts (e.g., wait-for-migrations.sh)
```

### 2. Authentication & Users
- **Model**: `CustomUser` in `apps/users/models.py`.
- **Constraint**: `username = None`, `USERNAME_FIELD = "email"`.
- **Flow**: Always use email/password.
- **Token**: Knox tokens with 10-hour TTL (`conf/settings.py`).
- **Creation**: Use `CustomUser.objects.create_user(email=...)`.

### 3. Celery Task Architecture
Use `BaseTaskWithRetry` for all tasks to ensure resilience.
```python
from apps.core.tasks import BaseTaskWithRetry
from celery import shared_task

@shared_task(bind=True, base=BaseTaskWithRetry)
def my_task(self, arg):
    # Auto-retries on Exception/KeyError
    # Max retries: 3, Backoff: 5s (exponential)
    pass
```

### 4. Logging & Request Tracking
- **Do NOT** use `print()`. Use `logger = logging.getLogger(__name__)`.
- **Request ID**: Automatically injected into every log entry via `RequestIDMiddleware`.
- **Context**: `user_id`, `client_ip`, `path`, `response_time` are available in logs.
- **Pattern**:
  ```python
  import logging
  logger = logging.getLogger(__name__)

  def my_view(request):
      logger.info(f"Processing order for user {request.user.email}")
  ```

### 5. API Documentation
- **Rule**: Every view MUST use `@extend_schema`.
- **Definition**: Define response structures in `schema.py` within each app.
```python
from drf_spectacular.utils import extend_schema
from .schema import MY_RESPONSE_SCHEMA

@extend_schema(responses=MY_RESPONSE_SCHEMA)
def my_view(request): ...
```

### 6. Type Safety
- **Tooling**: `mypy` for static analysis, `ruff` for linting/formatting.
- **Requirement**: All function signatures must be type-hinted.
- **Format**: `ruff` with line-length 90.
- **Example**:
```python
def get_dashboard_stats(user: CustomUser) -> dict[str, int]:
    ...
```

## Critical Workflows

### Docker & Make Commands
Always run commands via `make` or `docker compose exec backend`.
- **Start**: `make up`
- **Tests**: `make test` (runs `pytest`)
- **Migrations**: `make makemigrations` -> `make migrate`
- **Shell**: `make shell`
- **Logs**: `make logs`

### Testing
- **Framework**: `pytest` with `rest_framework.test.APITestCase`.
- **Pattern**: Mock logger to keep test output clean.
```python
from rest_framework.test import APITestCase
from unittest.mock import patch
import logging

class MyTests(APITestCase):
    def test_something(self):
        with patch.object(logging.Logger, "info") as mock_logger:
            # Action
            # Assert
```

### Dependency Management (uv)
- **Add Pkg**: `uv add <package>`
- **Sync**: `uv sync` (creates/updates lockfile)
- **Lock**: `uv lock`

## Configuration
- **Settings**: `conf/settings.py` uses `django-environ`.
- **Secrets**: Read from `.env`.
- **Timezone**: `America/Santiago`.
- **URLs**: App-specific URLs in `apps/<app>/urls.py`, included in `conf/urls.py`.
