# Changelog

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
