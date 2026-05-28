# AGENTS.md

## Commands

All Django commands run **inside Docker** (`docker compose exec backend`). Use the `make` shortcuts:

```sh
make up           # docker compose up
make test         # docker compose exec backend pytest
make test-cov     # pytest --cov
make migrate      # docker compose exec backend python manage.py migrate
make seed         # seed DB (creates admin@admin.com / admin)
make superuser    # createsuperuser
make shell        # shell_plus (django-extensions)
make logs         # logs -f backend
make logs-worker  # logs -f worker
make rebuild      # docker compose up --build
```

For a single test file or function:

```sh
docker compose exec backend pytest apps/users/tests/test_user_model.py
docker compose exec backend pytest apps/users/tests/test_user_model.py::test_create_user
```

## Lint & Typecheck

**No CI enforces lint/typecheck.** Run manually before committing:

```sh
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

Ruff fixes (`I` isort, `B` bugbear, `E`/`F` pycodestyle/pyflakes). Line-length 90, double quotes.

## Architecture

- **Django settings:** `conf/settings.py` — `DJANGO_SETTINGS_MODULE=conf.settings`
- **Test settings:** `conf/test_settings.py` — swaps `RequestIDMiddleware`/`RequestIDFilter` for mocks, relaxes login throttle to 1000/min
- **Apps:** `apps/users/` (CustomUser, auth), `apps/core/` (ping, middleware, tasks, seed — no models)
- **AUTH_USER_MODEL:** `users.CustomUser` — email-based login, `username=None`, `USERNAME_FIELD='email'`
- **Auth:** JWT tokens (simplejwt, HS256, access 1hr + refresh 24hr, `Bearer` prefix). Admin creates users via `/api/v1/auth/create/`.
- **Admin URL:** `/admin-panel/` (not `/admin/`)
- **Celery:** Django `DatabaseScheduler` for beat. Worker/beat wait for migrations via `scripts/wait-for-migrations.sh`.
- **Backend Docker entrypoint auto-runs `migrate`** on every start — no manual step needed in Docker.

## Testing

- `DJANGO_SETTINGS_MODULE=conf.test_settings` is hardcoded in `pytest.ini`.
- `pytest.ini` has **no addopts** — `docs/testing.md` shows `--reuse-db --nomigrations --cov` etc. but these are **stale/not in the actual config**. Pass flags explicitly.
- Tests use DRF `APITestCase` + `unittest.mock.patch` for mocks (not pytest-mock typically).
- Database is real Postgres (no sqlite in-memory). CI uses `postgres:alpine` service.
- `/api/v1/core/fire-task/` endpoint is marked for removal — don't write tests for it.

## Python Version Mismatch

Runtime is **Python 3.14** (`.python-version`, Dockerfile, CI), but `pyproject.toml` ruff/mypy target **py313**. Keep both in mind.

## Dependency Management

Always use `uv`, not pip:

```sh
uv add <pkg>
uv remove <pkg>
uv lock --upgrade
```
