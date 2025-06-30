## Brief overview
This document outlines rules and best practices for Django backend development, covering framework usage, project structure, testing, and documentation.

## Framework & Core Dependencies
- Use Django 5.2+ with Django REST Framework for APIs
- Default to PostgreSQL for database operations
- Implement Redis caching for expensive operations
- Use django-rest-knox for authentication
- Document APIs using drf-spectacular

## Project Structure
- Follow Django's recommended project layout strictly
- Keep apps modular with single responsibilities
- Place test files in each app's `tests` directory
- Implement RESTful API patterns consistently

## Development Practices
- Strictly follow Django's security standards
- Use DRF viewsets and serializers for all endpoints
- Implement proper authentication with knox
- Cache expensive operations using Redis
- Document APIs with OpenAPI/Swagger via drf-spectacular

## Testing Requirements
- Write comprehensive unit tests for all features
- Achieve minimum test coverage as specified
- Include positive and negative test scenarios
- Maintain test files alongside the code they test

## Documentation Standards
- Include docstrings for all important classes/methods
- Document API endpoints thoroughly
- Keep documentation up-to-date with code changes
- Reference official Django/DRF documentation

## Additional Guidelines
- Prefer Django's built-in solutions over custom ones
- Maintain backward compatibility when making changes
- Validate all user input thoroughly
- Implement proper error handling and logging
