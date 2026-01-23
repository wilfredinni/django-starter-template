# Logging System

This section details the logging system implemented in the Django Starter Template, which is designed for high-performance production environments using 12-Factor App methodology.

## Overview

The logging system is configured in `conf/settings.py` to stream all events to `stdout` (Console) in structured JSON format. This eliminates the need for managing local log files and integrating easily with modern container logging drivers (Docker, Kubernetes) and aggregators (Datadog, Splunk, CloudWatch).

## Key Features

*   **JSON Format**: All logs are formatted as JSON, enabling machine readability and easier parsing.
*   **Console Only**: Adheres to "logs as event streams" philosophy. No files are written to disk.
*   **Unified Logger**: Centralized logger strategy simplifies configuration and prevents "lost" logs.
*   **Request Tracing**: A modern, async-safe `RequestIDMiddleware` assigns a unique `request_id` to each request. This is stored in `ContextVars` (immune to thread-bleeding issues) and injected into every log line.
*   **Automatic Context**: Every log entry automatically includes:
    *   `request_id`
    *   `client_ip`
    *   `user_id` (if authenticated)
    *   `path`
    *   `response_time` (for completed requests)

## Log Levels & Categories

The system uses three primary logger categories:

1.  **Root (`""`)**: format catching all third-party libraries.
2.  **Framework (`"django"`)**: Captures internal framework events (DB queries, generic errors).
3.  **Application (`"apps"`)**: Captures your business logic logs.

## How to Log in Your Code

Do not use `print()`. Use the standard Python logging module with the `__name__` convention:

```python
import logging
logger = logging.getLogger(__name__)

def my_view(request):
    logger.info("Processing order %s", order_id)
    try:
        ...
    except ValueError as e:
        logger.warning("Invalid input received: %s", e)
```

**Note:** Always use lazy interpolation (e.g., `logger.info("Msg %s", var)`), NOT f-strings, to improve performance.

## Example Log Entry

```json
{
    "asctime": "2026-01-23 20:29:08,372",
    "levelname": "INFO", 
    "module": "apps.users.views", 
    "message": "User admin@admin.com logged in.", 
    "request_id": "2cecc66f-6cf1-4417-bbc8-af862bba999e", 
    "user_id": "anonymous", 
    "client": "192.168.97.1",
    "path": "/auth/login/"
}
```
