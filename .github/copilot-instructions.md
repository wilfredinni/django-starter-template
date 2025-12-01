# Django Starter Template - AI Development Guide

## Architecture Overview

This is a **production-ready Django 5.1+ API template** with:
- **Custom email-based authentication** using `django-rest-knox` (no username field)
- **Async task processing** via Celery + Redis with automatic retry patterns
- **Structured JSON logging** with request ID tracking and performance metrics
- **Auto-generated OpenAPI docs** via `drf-spectacular`

## Key Development Patterns

### Project Structure
```
apps/                    # Django apps (users, core)
├── users/               # Custom user model with email auth
├── core/                # Shared utilities, middleware, tasks
conf/                    # Django settings and configuration
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

### Docker Compose Commands
```bash
# Start all services
docker compose up

# Run migrations
docker compose exec backend python manage.py migrate

# Create migrations
docker compose exec backend python manage.py makemigrations

# Create superuser
docker compose exec backend python manage.py createsuperuser

# Seed database
docker compose exec backend python manage.py seed

# Run Django shell
docker compose exec backend python manage.py shell

# View logs
docker compose logs -f backend
docker compose logs -f worker
docker compose logs -f beat
```

### Testing
- Use **pytest** with `pytest.ini` configuration
- Tests in `apps/{app}/tests/` directories
- Run tests: `docker compose exec backend pytest`
- Coverage: `docker compose exec backend pytest --cov`
- Example pattern: `test_create_user_view.py` with `APITestCase`
- Mock logging calls in tests for verification

### Environment Setup
- Use `.env.example` as template for `.env` file
- PostgreSQL + Redis containers included via Docker Compose
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
- **Use docker compose exec** for running Django commands in containers
- **Test authentication flows** - most endpoints require Knox tokens
- **Document APIs** - use `drf-spectacular` decorators for schema generation
- **Handle task failures** - leverage `BaseTaskWithRetry` for resilience
