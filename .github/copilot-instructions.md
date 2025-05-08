Technical Requirements and Communication Standards for Django Backend Development

**Framework & Core Dependencies:**
- Django 5.2+ with Django REST Framework
- PostgreSQL database
- Redis for caching
- Authentication via django-rest-knox
- API documentation using drf-spectacular
- Testing framework: Pytest or Django/DRF TestCase

**Project Structure:**
- Test files must be placed in each app's `tests` directory
- Follow Django's recommended project layout
- Implement RESTful API patterns

**Development Guidelines:**
1. All implementations must follow Django's best practices and security standards
2. Use Django REST Framework viewsets and serializers when building APIs
3. Implement proper authentication and permission checks using knox
4. Cache expensive operations using Redis
5. Document all APIs using OpenAPI/Swagger via drf-spectacular

**Testing Requirements:**
1. Write comprehensive unit tests for all features
2. Follow Pytest conventions and patterns
3. Achieve minimum test coverage as per project standards
4. Include both positive and negative test scenarios

**Documentation:**
1. Reference official Django and DRF documentation
2. Include docstrings for all classes and methods that have an important role

3. Document API endpoints using drf-spectacular decorators

**Response Format:**
1. Provide direct, implementation-focused answers
2. Highlight any missing information needed for implementation
3. Include code examples only when explicitly requested
4. Format code according to PEP 8 standards

- Utilize context7 MCP for current documentation when applicable

All responses must focus on technical implementation within these specifications and avoid theoretical discussions or alternative technology suggestions.
