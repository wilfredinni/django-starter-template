# Core App

This section details the functionalities and API endpoints provided by the Core application (`apps/core/`). The Core app serves as a foundation for common utilities, middleware, and base tasks within the Django Starter Template.

## Functionalities

The `apps/core` directory contains:

*   **Middleware**: Custom middleware, such as `RequestIDMiddleware`, for adding request-specific information (e.g., request ID, client IP, response time) to logs and responses.
*   **Tasks**: Base Celery task classes, like `BaseTaskWithRetry`, which provide common functionalities such as automatic retries for background tasks.
*   **Schema**: Common OpenAPI schema definitions and examples used across different API endpoints.
*   **Management Commands**: Custom Django management commands (e.g., `seed` command for populating the database with sample data).

## Endpoints

These endpoints are prefixed with `/core/`.

### Ping

GET /core/ping/

A simple endpoint to check if the server is running.

**Success Response (200 OK):**

```json
{
    "ping": "pong"
}
```

### Fire Task

GET /core/fire-task/

Triggers a sample Celery task.

**Success Response (200 OK):**

```json
{
    "task": "Task fired"
}
```