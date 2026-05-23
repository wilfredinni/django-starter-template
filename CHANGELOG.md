# Changelog

## [Unreleased] - 2026-05-23

### Added

- AGENTS.md with AI coding assistant instructions (commands, architecture, testing conventions)
- AI skills installed from vintasoftware/django-ai-plugins (django-expert, django-celery-expert)
- skills-lock.json for tracking installed AI skill versions and provenance
- AI-Assisted Development documentation page (`docs/ai.md`) with mkdocs nav entry
- AI tooling features and links added to `docs/index.md` and `README.md`

### Removed

- Removed GitHub Copilot prompts
- Removed AI tools documentation
- Removed VS Code settings

### Changed

- Pinned PostgreSQL image to version 18-alpine
- Changed Makefile shell command to use `shell_plus`
