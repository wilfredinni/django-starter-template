# Changelog

## [0.6.1](https://github.com/wilfredinni/django-starter-template/releases/tag/0.6.1) - 2026-10-24

Security hardening, Docker improvements, and dependency updates

### Added

- Service-specific health checks for Django, Celery worker, Celery beat, and the documentation preview
- Regression tests for login throttling, request context cleanup, safe seeding, and production settings
- Collection name in the Noodle API collection settings

### Changed

- Docker now uses a multi-stage build with digest-pinned Python and uv images, keeping build tools out of the non-root runtime
- Compose ports bind to localhost, source directories mount read-only, and all application services build the shared image on startup
- Redis requires a unique URL-safe `REDIS_PASSWORD` in `.env`; cache and Celery use separate Redis databases
- `make makemigrations` and `make docs-serve` use dedicated one-shot services; documentation and HTML coverage builds copy their output back to the host
- Production requires explicit `ALLOWED_HOSTS`, `REDIS_URL`, and `CELERY_BROKER_URL`; forwarded client IP headers are ignored unless proxy trust is configured
- Updated locked dependencies, including Django 6.0.9, Psycopg 3.3.6, Tornado 6.6, and urllib3 2.8.0

### Fixed

- Enabled default API throttles and limited login attempts by both IP and normalized target account, preventing token, forwarded-header, and source-IP changes from bypassing limits
- Request logging validates the direct peer IP and resets request-scoped context after successful and failed requests
- Database seeding is restricted to `DEBUG=True` and generates unique random passwords for sample users
- Debug Toolbar trusts loopback addresses only instead of automatically trusting Docker gateway addresses
- Docker and CI dependency installation enforce lockfile hashes; CI uses a pinned setup-uv action instead of a remote shell installer

### Removed

- Unauthenticated `/api/v1/core/fire-task/` endpoint and its example Celery task
- Hard-coded seed credentials and the `seed --superuser` option; use `make superuser` to create an administrator
- Tracked Noodle UI state and default credentials from the local API collection environment

## [0.6.0](https://github.com/wilfredinni/django-starter-template/releases/tag/0.6.0) - 2026-08-25

Noodle API collection, Python 3.14 tooling target, and dependency updates

### Added

- [Noodle](https://noodlerest.dev) API collection (`api-collection/`) covering all `v1` endpoints: auth (create user, login, logout, logout all) and profile management, plus a `core/ping` health check
- Local environment for the collection (`base_url`, seed credentials, Knox token secret)
- API Collection documentation page (`docs/noodle.md`) with installation, usage, and authentication guide
- Noodle feature added to `README.md` and `docs/project_structure.md`

### Changed

- ruff `target-version` and mypy `python_version` updated from `py313` to `py314`
- AGENTS.md cleaned up and streamlined
- Updated dependencies to their latest versions

## [0.5.2](https://github.com/wilfredinni/django-starter-template/releases/tag/0.5.2) - 2026-05-23

AI tooling setup, infra improvements, and dependency updates

### Added

- AGENTS.md with AI coding assistant instructions (commands, architecture, testing conventions)
- AI skills installed (django-expert, django-celery-expert)
- skills-lock.json for tracking installed AI skill versions and provenance
- AI-Assisted Development documentation page (`docs/ai.md`) with mkdocs nav entry
- AI tooling features and links added to `docs/index.md` and `README.md`
- TODO-guided customization steps documented in `README.md` and `docs/index.md`

### Removed

- Removed GitHub Copilot prompts
- Removed AI tools documentation
- Removed VS Code settings
- Removed `SECURITY.md`, `notebook.ipynb`, `renovate.json`

### Changed

- Pinned PostgreSQL image to version 18-alpine
- Changed Makefile shell command to use `shell_plus`
- Bumped project version to `0.5.2`
- Updated dependencies
