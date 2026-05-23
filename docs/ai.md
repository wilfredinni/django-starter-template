# AI-Assisted Development

## Overview

The Django Starter Template includes built-in support for AI coding agents such as [OpenCode](https://opencode.ai), GitHub Copilot, and other LLM-powered tools. These integrations help AI assistants understand the project's conventions, commands, and architecture—producing higher quality code with less context-building overhead.

## AGENTS.md

The `AGENTS.md` file at the project root provides AI coding agents with essential context about how this project works. It covers:

- **Commands** — All Django commands run inside Docker via `make` shortcuts (`make test`, `make migrate`, `make seed`, etc.) or raw `docker compose exec backend` commands.
- **Lint & Typecheck** — Ruff and mypy configuration details (line-length 90, double quotes, no CI enforcement).
- **Architecture** — Django settings module, test settings overrides, app layout (`apps/users`, `apps/core`), custom user model (email-based, Knox tokens), admin URL (`/admin-panel/`), Celery with `DatabaseScheduler`.
- **Testing** — Test settings hardcoded in `pytest.ini`, no default addopts, DRF `APITestCase` + `unittest.mock.patch` patterns, real Postgres database.
- **Python Version Mismatch** — Runtime is Python 3.14, but lint targets Python 3.13.
- **Dependency Management** — Always use `uv`, not pip.

When an AI agent reads this file, it gains immediate awareness of project-specific conventions without needing to scan the entire codebase.

## AI Skills

Skills are modular, versioned bundles of domain-specific reference documentation that AI agents load on-demand. They enable agents to draw from curated best-practice guides for Django and Celery development.

The project ships with two skills installed from [vintasoftware/django-ai-plugins](https://github.com/vintasoftware/django-ai-plugins):

### django-expert

Expert Django backend development guidance covering:

- Model design and ORM patterns
- View implementation (function-based, class-based, DRF viewsets)
- Django REST Framework API development
- Query optimization and performance tuning
- Authentication and permissions
- Testing strategies and patterns
- Security best practices

Reference files: `models-and-orm.md`, `views-and-urls.md`, `drf-guidelines.md`, `testing-strategies.md`, `security-checklist.md`, `performance-optimization.md`, `production-deployment.md`.

### django-celery-expert

Expert guidance for asynchronous task processing with Celery, covering:

- Django integration patterns (transaction safety, ORM usage, request correlation)
- Task design patterns (calling patterns, chains/groups/chords, idempotency)
- Configuration (broker setup, result backends, queue routing)
- Error handling (retries, backoff, dead letter queues, timeouts)
- Periodic tasks with Celery Beat (crontab, dynamic schedules, timezone handling)
- Monitoring and observability (Flower, Prometheus, logging)
- Production deployment (scaling, supervision, containers, health checks)

Reference files: `django-integration.md`, `task-design-patterns.md`, `configuration-guide.md`, `error-handling.md`, `periodic-tasks.md`, `monitoring-observability.md`, `production-deployment.md`.

## skills-lock.json

The `skills-lock.json` file tracks installed skills and their provenance:

```json
{
  "version": 1,
  "skills": {
    "django-expert": {
      "source": "vintasoftware/django-ai-plugins",
      "sourceType": "github",
      "skillPath": "plugins/django-expert/skills/SKILL.md",
      "computedHash": "a6b8c224..."
    },
    "django-celery-expert": {
      "source": "vintasoftware/django-ai-plugins",
      "sourceType": "github",
      "skillPath": "plugins/django-celery-expert/skills/SKILL.md",
      "computedHash": "31eb59e3..."
    }
  }
}
```

This lock file ensures skills are reproducible across environments. The `computedHash` field verifies skill integrity—if the upstream skill changes, the hash mismatch signals a review is needed before updating.

## Installing Additional Skills

To add more skills from the [django-ai-plugins](https://github.com/vintasoftware/django-ai-plugins) repository or other sources, use your AI agent's skill installation mechanism. Skills are stored under `.agents/skills/` and tracked in `skills-lock.json`.

## How It Works

1. An AI coding agent reads `AGENTS.md` to understand project conventions and commands.
2. When the agent encounters a Django or Celery task, it loads the relevant skill (e.g., `django-expert` for model creation, `django-celery-expert` for background task design).
3. The skill provides curated reference documentation that guides the agent toward idiomatic, production-ready implementations.
4. `skills-lock.json` ensures the exact same skill versions are used across all developer environments.
