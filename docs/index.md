# Django Starter Template Documentation

Welcome to the documentation for the Django Starter Template. This document provides a comprehensive guide to understanding, developing, and using this template.

# Explanation

This document provides a detailed explanation of the Django Starter Template's architecture, key components, and core concepts.

## Project Structure

The project is organized into several directories, each with a specific purpose:

*   **`.devcontainer/`**: Contains configuration for developing inside a Docker container, ensuring a consistent development environment.
*   **`.github/`**: Holds GitHub-specific files, including CI/CD workflows and issue templates.
*   **`.vscode/`**: Stores VS Code settings for the project.
*   **`apps/`**: This is where the core application logic resides. It's divided into smaller, reusable Django apps:
    *   **`core/`**: Contains core functionality, such as custom management commands, base Celery tasks, and API schema definitions.
    *   **`users/`**: Manages user authentication and related models, views, and schemas.
*   **`conf/`**: The project's configuration hub. It includes the main settings file, Celery configuration, and test-specific settings.
*   **`logs/`**: Stores application logs, including general, error, and security logs.
*   **`scripts/`**: Contains utility scripts for various development tasks.

## Key Technologies

The template is built on a foundation of modern and robust technologies:

*   **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
*   **Django Rest Framework (DRF)**: A powerful and flexible toolkit for building Web APIs.
*   **PostgreSQL**: A powerful, open-source object-relational database system.
*   **Redis**: An in-memory data structure store, used as a message broker for Celery and for caching.
*   **Celery**: An asynchronous task queue/job queue based on distributed message passing.
*   **drf-spectacular**: A library for generating OpenAPI 3 schemas for Django Rest Framework APIs.

## Core Concepts

### Custom User Model

The template uses a custom user model that authenticates users with their email address instead of a username. This is a common practice in modern web applications.

### Token-Based Authentication

Authentication is handled by `knox`, which provides a secure and scalable token-based authentication system. Tokens are SHA-512 hashed and have a configurable expiration time.

### Background Tasks

Asynchronous tasks are managed by Celery, with Redis as the message broker. The template includes a base task class with automatic retry capabilities, making it easy to create robust and reliable background tasks.

### Centralized Logging

The project features a centralized logging system that outputs structured logs in JSON format. This makes it easy to parse, search, and analyze logs, especially in a production environment.