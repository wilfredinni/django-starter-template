# Environment Setup

This section explains how environment variables are used in the Django Starter Template and how to configure your project for both development and production environments.

## Environment Variables

Environment variables are a crucial part of modern application development, allowing you to configure your application's behavior without modifying the codebase. This is especially important for sensitive information (like API keys, database credentials) and for settings that vary between development, testing, and production environments.

This project uses the `django-environ` library to manage environment variables. It reads variables from a `.env` file located in the project's root directory.

### `.env.example`

The `.env.example` file serves as a template for your `.env` file. It lists all the environment variables that your project expects, along with example values and comments explaining their purpose. **Never commit your actual `.env` file to version control.**

```ini
# --------------------------------------------------------------------------------
# ⚡ Basic Config: for development and testing.
# --------------------------------------------------------------------------------
DEBUG=True
DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres
DJANGO_SECRET_KEY=django-insecure-wlgjuo53y49%-4y5(!%ksylle_ud%b=7%__@9hh+@$d%_^y3s!


# --------------------------------------------------------------------------------
# 📧 Email Config: optional and can be copied if needed.
# --------------------------------------------------------------------------------
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=user@user.com
EMAIL_HOST_PASSWORD=myverystrongpassword


# --------------------------------------------------------------------------------
# 🔐 Security Config: for production or testing the production settings locally.
# --------------------------------------------------------------------------------
ALLOWED_HOSTS=mysite.com,mysite2.com
CORS_ALLOWED_ORIGINS=mysite.com,mysite2.com
SENTRY_DSN=https://examplePublicKey@o0.ingest.sentry.io/0
```

To set up your environment, copy `.env.example` to `.env` and fill in the appropriate values:

```bash
cp .env.example .env
```

## Development Environment

For local development, the following environment variables are typically set:

*   `DEBUG=True`: Enables Django's debug mode, providing detailed error pages and auto-reloading.
*   `DATABASE_URL`: Specifies the connection string for your local database (e.g., PostgreSQL running in Docker).
*   `DJANGO_SECRET_KEY`: A secret key for development purposes. You can use the example one provided in `.env.example`.

When using the Dev Container setup (recommended), the `.env` file is automatically created and configured for a development environment.

## Production Environment

For production deployments, it is critical to configure your environment variables securely and appropriately:

*   `DEBUG=False`: **Always set to `False` in production.** This disables debug mode, preventing sensitive information from being exposed in error pages.
*   `DJANGO_SECRET_KEY`: Generate a strong, unique secret key and store it securely. **Never use the development secret key in production.**
*   `ALLOWED_HOSTS`: A comma-separated list of domain names that your Django application will serve. **Do not use `*` in production.**
*   `DATABASE_URL`: The connection string for your production database.
*   `CORS_ALLOWED_ORIGINS`: A comma-separated list of origins that are allowed to make cross-origin requests to your API. **Do not use `CORS_ALLOW_ALL_ORIGINS=True` in production.**
*   `SENTRY_DSN`: Your Sentry Data Source Name (DSN) for error tracking and performance monitoring.
*   `EMAIL_HOST`, `EMAIL_USE_TLS`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Configure these for sending emails from your production environment.

### Example Production `.env` (Conceptual)

```ini
DEBUG=False
DJANGO_SECRET_KEY=your_very_long_and_secure_production_secret_key
ALLOWED_HOSTS=api.yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@db.yourdomain.com:5432/prod_db
CORS_ALLOWED_ORIGINS=https://www.yourdomain.com,https://app.yourdomain.com
SENTRY_DSN=https://your_sentry_public_key@o0.ingest.sentry.io/0
EMAIL_HOST=smtp.sendgrid.net
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your_sendgrid_api_key
```

## Managing Environment Variables

It is recommended to use a tool or service provided by your deployment platform (e.g., Docker Compose, Kubernetes, Heroku, AWS Elastic Beanstalk) to manage and inject environment variables into your production environment. This ensures that sensitive information is not hardcoded or exposed in your codebase.
