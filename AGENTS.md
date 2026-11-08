# AGENTS.md

## Commands

All Django commands run **inside Docker** (`docker compose exec backend`). Use the `make` shortcuts:

```sh
make up           # docker compose up
make test         # docker compose exec backend pytest
make test-cov     # pytest --cov
make test-html    # pytest --cov --cov-report=html
make migrate      # docker compose exec backend python manage.py migrate
make seed         # seed sample users (DEBUG only; random passwords)
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

Compose requires a URL-safe `REDIS_PASSWORD` in `.env` and binds ports to loopback.
Source mounts are read-only. Use `make makemigrations` for a temporary writable app
mount; use `make docs-serve` to publish the documentation port only while needed.

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

## Noodle API Checks

- `.github/workflows/test.yml` runs the **Noodle API collections** job alongside the Python tests. It uses a pinned `wilfredinni/setup-noodle` v1.0.0 commit to install Noodle v0.10.4, starts the API with Docker Compose, and creates a disposable administrator.
- `api-collection/settings.yml` sets `auth/login` as the setup hook. Each collection run logs in and captures `$token` in memory; collection runs do not persist captures.
- CI uses `api-collection/.environments/ci.env`. Supply the declared `password` and `password2` secrets through process environment variables, as the workflow does. **Do not declare `token` in `ci.env`**: environment loading would query the unavailable Linux keyring before the login hook can capture it.
- Run logout endpoints separately so token revocation cannot break the other checks. With the CI stack and administrator ready, run:

```sh
noodle collection run api-collection auth/create-user core/ profile/ \
  --env ci --fail-fast --reporter junit --output noodle-api.xml
noodle collection run api-collection auth/logout \
  --env ci --fail-fast --reporter junit --output noodle-logout.xml
noodle collection run api-collection auth/logout-all \
  --env ci --fail-fast --reporter junit --output noodle-logout-all.xml
```

- These checks create a user and update the administrator's profile. Use a disposable database; local runs need an unused `new_user_email` and configured local credentials (see `docs/noodle.md`). `request run` does not execute the setup hook.
- CI uploads available JUnit reports as `noodle-api-results`, including reports from failed runs. Noodle does not overwrite reports; use new output filenames when repeating checks outside a fresh CI checkout.

## Dependency Management

Always use `uv`, not pip:

```sh
uv add <pkg>
uv remove <pkg>
uv lock --upgrade
```
