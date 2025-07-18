# Django Starter Template - AI Development Guide

## Architecture Overview

This is a **production-ready Django 5.1+ API template** with:
- **Custom email-based authentication** using `django-rest-knox` (no username field)
- **Async task processing** via Celery + Redis with automatic retry patterns
- **Structured JSON logging** with request ID tracking and performance metrics
- **Auto-generated OpenAPI docs** via `drf-spectacular`
- **DevContainer setup** for consistent development environments

## Key Development Patterns

### Project Structure
```
apps/                    # Django apps (users, core)
├── users/               # Custom user model with email auth
├── core/                # Shared utilities, middleware, tasks
conf/                    # Django settings and configuration
scripts/                 # Poetry-managed CLI commands
```

### Custom User Implementation
- **No username field** - uses `CustomUser(AbstractUser)` with `email` as `USERNAME_FIELD`
- Located in `apps/users/models.py` with `CustomUserManager`
- All auth flows expect email-based authentication

### Celery Task Architecture
```python
# Use BaseTaskWithRetry for all background tasks
@shared_task(bind=True, base=BaseTaskWithRetry)
def your_task(self):
    # Auto-retry up to 3 times with exponential backoff
```

### Logging & Request Tracking
- All requests get unique IDs via `RequestIDMiddleware`
- Use structured logging: `logger = logging.getLogger("django.info")`
- Performance metrics automatically logged in thread-local storage
- Separate log files: `app.log`, `error.log`, `info.log`, `security.log`

### API Development Standards
- Use `@extend_schema()` decorators for all endpoints (auto-documentation)
- Implement rate limiting with custom throttle classes
- Authentication via Knox tokens with `Bearer` prefix
- Return structured JSON responses consistently

## Essential Commands

### Poetry Scripts (use these over direct manage.py)
```bash
poetry run server           # python manage.py runserver
poetry run makemigrations   # python manage.py makemigrations
poetry run migrate          # python manage.py migrate
poetry run worker           # Start Celery worker
poetry run beat             # Start Celery beat scheduler
poetry run create_dev_env   # Generate .env file
poetry run seed             # Seed database with test data
```

### Testing
- Use **pytest** with `pytest.ini` configuration
- Tests in `apps/{app}/tests/` directories
- Example pattern: `test_create_user_view.py` with `APITestCase`
- Mock logging calls in tests for verification

### Environment Setup
- **DevContainer required** - use "Reopen in Container"
- Auto-generates `.env` with `create_dev_env` script
- PostgreSQL + Redis containers included
- Uses `DATABASE_URL` environment variable pattern

## Integration Points

### Knox Authentication Flow
```python
# Token creation returns user profile via UserProfileSerializer
# Configure in settings: REST_KNOX['USER_SERIALIZER']
# Tokens expire after 10 hours by default
```

### Celery + Redis
- **Background tasks**: Inherit from `BaseTaskWithRetry`
- **Beat scheduling**: Use `django-celery-beat` for periodic tasks
- **Results backend**: `django-celery-results` stores task outcomes

### Request Middleware Chain
1. Security & CORS headers
2. `RequestIDMiddleware` - adds unique request tracking
3. Knox authentication
4. Custom logging with performance metrics

## File Naming Conventions
- Tests: `test_{feature}_view.py`, `test_{model}_model.py`
- Tasks: Define in `apps/{app}/tasks.py`
- URLs: App-level `urls.py` included in `conf/urls.py`
- Settings: Environment-based config in `conf/settings.py`

## Critical Implementation Notes
- **Never use username** - all user references should use email
- **Always use Poetry scripts** instead of direct `python manage.py`
- **Test authentication flows** - most endpoints require Knox tokens
- **Document APIs** - use `drf-spectacular` decorators for schema generation
- **Handle task failures** - leverage `BaseTaskWithRetry` for resilience
