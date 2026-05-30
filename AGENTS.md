# AGENTS.md

## Commands

All Django commands run **inside Docker** (`docker compose exec backend`). Use the `make` shortcuts:

```sh
make up           # docker compose up
make test         # docker compose exec backend pytest
make test-cov     # pytest --cov
make test-html    # pytest --cov --cov-report=html
make migrate      # docker compose exec backend python manage.py migrate
make seed         # seed DB (creates admin@admin.com / admin)
make superuser    # createsuperuser
make shell        # shell_plus (django-extensions, only in DEBUG)
make logs         # logs -f backend
make logs-worker  # logs -f worker
make logs-beat    # logs -f beat
make rebuild      # docker compose up --build
```

Single test file or function:

```sh
docker compose exec backend pytest apps/users/tests/test_user_model.py
docker compose exec backend pytest apps/users/tests/test_user_model.py::test_create_user
```

**Important:** The backend entrypoint auto-runs `migrate` on every start. No manual migrate step needed in Docker.

## Lint & Typecheck

**No CI enforces lint/typecheck.** Run manually before committing:

```sh
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

Ruff selects `E`/`F`/`I`/`B`, line-length 90, double quotes, target `py314`. Mypy targets `python_version = "3.14"` with django-stubs + mypy-drf-plugin.

## Architecture

- **Django settings:** `conf/settings.py` (`DJANGO_SETTINGS_MODULE=conf.settings`)
- **Test settings:** `conf/test_settings.py` — swaps RequestIDMiddleware/RequestIDFilter for mocks, uses `LocMemCache` (throttle state resets per run), relaxes all throttle rates to 1000/min
- **Apps:** `apps/users/` (CustomUser, auth), `apps/core/` (ping, middleware, tasks, seed — no models)
- **AUTH_USER_MODEL:** `users.CustomUser` — email-based, `username=None`, `USERNAME_FIELD='email'`
- **Auth:** Knox tokens (sha512, 64 chars, 10hr TTL, `Bearer` prefix). Admin creates users via `/api/v1/auth/create/`
- **Admin URL:** `/admin-panel/` (not `/admin/`)
- **Celery:** app name `"worker"` in `conf/celery.py`, `celery -A conf` for CLI. Django `DatabaseScheduler` for beat. Worker/beat wait for migrations via `scripts/wait-for-migrations.sh`
- **Package layout:** `pyproject.toml` sets `packages = ["apps", "conf"]` — internal imports use `apps.core.`, `apps.users.`, `conf.settings`

## Testing

- `DJANGO_SETTINGS_MODULE=conf.test_settings` is hardcoded in `pytest.ini`
- `pytest.ini` includes `addopts = --reuse-db --nomigrations` — these flags are always active
- Test database is real Postgres (Docker service). There is no sqlite in-memory fallback
- Tests use DRF `APITestCase` + `unittest.mock.patch` for mocks (not pytest-mock fixtures)
- `conf/test_utils.py` provides mock middleware/filter for RequestID logging context
- `/api/v1/core/fire-task/` endpoint is example code marked for removal — skip writing tests for it


## Dependency Management

Always use `uv`, not pip:

```sh
uv add <pkg>
uv remove <pkg>
uv lock --upgrade
```
