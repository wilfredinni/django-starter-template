# Project Settings

This document provides an extensive guide to the `conf/settings.py` file, which centralizes the configuration for the Django Starter Template. Understanding these settings is crucial for customizing and deploying your application.

## Environment Variables (`django-environ`)

The project uses `django-environ` to manage environment variables, allowing sensitive information and deployment-specific configurations to be kept out of version control. Variables are loaded from a `.env` file in the project root.

```python
import environ

env = environ.Env()
root_path = environ.Path(__file__) - 2
env.read_env(str(root_path.path(".env")))
```

*   `env = environ.Env()`: Initializes the environment reader.
*   `root_path`: Defines the base directory for relative paths, calculated as two levels up from the `settings.py` file.
*   `env.read_env()`: Reads variables from the `.env` file. This function is called without arguments, so it looks for `.env` in the current working directory or parent directories.

## Basic Configuration

These are fundamental Django settings.

*   `ROOT_URLCONF`: Specifies the root URL configuration module. **Default:** `conf.urls`. This tells Django where to find the main URL patterns for your project.
*   `WSGI_APPLICATION`: The full Python path to the WSGI application object. **Default:** `conf.wsgi.application`. This is the entry point for WSGI-compatible web servers.
*   `DEBUG`: A boolean that turns debug mode on or off. **Default:** `False` (loaded from `env.bool("DEBUG", default=False)`). When `True`, Django provides detailed error pages, reloads code on changes, and enables other development-specific features. **Must be `False` in production for security and performance reasons.**

## Time & Language

Standard settings for localization and time zones.

*   `LANGUAGE_CODE`: The language code for this installation. **Default:** `en-us`. This affects the default language for Django's built-in messages and templates.
*   `TIME_ZONE`: The time zone for this installation. **Default:** `UTC`. This is the time zone that Django will use for all datetime objects unless a specific timezone is activated.
*   `USE_I18N`: A boolean that specifies whether Django's internationalization system should be enabled. **Default:** `True`. When `True`, Django will look for translation files.
*   `USE_TZ`: A boolean that specifies whether Django's timezone support should be enabled. **Default:** `True`. When `True`, Django stores datetimes in UTC in the database and converts them to the user's local time zone for display.

## Security and Users

This section covers critical security configurations and user model settings.

*   `SECRET_KEY`: A secret key for a particular Django installation. **Default:** Loaded from the `DJANGO_SECRET_KEY` environment variable. This is used to provide cryptographic signing and should be a unique, unpredictable value. **Must be kept secret and loaded from environment variables.**

    ```python
    SECRET_KEY = env("DJANGO_SECRET_KEY")
    ```

*   `ALLOWED_HOSTS`: A list of strings representing the host/domain names that this Django site can serve. **Default:** `["*"]` (loaded from `env.list("ALLOWED_HOSTS", default=["*"])`). This is a security measure to prevent HTTP Host header attacks. **In production, specify your exact domain names (e.g., `["example.com", "www.example.com"]`) and never use `"*"` for security.**

    ```python
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
    ```

*   `AUTH_USER_MODEL`: Specifies the custom user model to use. **Default:** `users.CustomUser`. This allows you to extend Django's default user model with custom fields and behaviors.
*   `MIN_PASSWORD_LENGTH`: Minimum length for user passwords. **Default:** `8` (loaded from `env.int("MIN_PASSWORD_LENGTH", default=8)`). This is used by the password validation system.
*   `PASSWORD_HASHERS`: A list of password hashing algorithms used for storing user passwords. Django will try them in order until one works. **Default:** A list including `ScryptPasswordHasher`, `PBKDF2PasswordHasher`, `PBKDF2SHA1PasswordHasher`, `Argon2PasswordHasher`, and `BCryptSHA256PasswordHasher`. This provides strong password security.
*   `AUTH_PASSWORD_VALIDATORS`: Configures password validation rules. **Default:** Includes validators for user attribute similarity, minimum length, common passwords, and numeric passwords. You can customize these to enforce stronger password policies.

### Security Headers

*   `SECURE_BROWSER_XSS_FILTER`: A boolean that enables the X-XSS-Protection header. **Default:** `True`. This helps protect against Cross-Site Scripting (XSS) attacks.
*   `SECURE_CONTENT_TYPE_NOSNIFF`: A boolean that enables the X-Content-Type-Options header. **Default:** `True`. This prevents browsers from MIME-sniffing a response away from the declared content-type.
*   `X_FRAME_OPTIONS`: Prevents clickjacking by setting the X-Frame-Options header. **Default:** `DENY`. This means the page cannot be displayed in a frame.
*   `CSRF_COOKIE_SECURE`: A boolean that determines whether the CSRF cookie should be sent only over HTTPS. **Default:** `True` if `DEBUG` is `False`, `False` otherwise. **Should be `True` in production.**
*   `SESSION_COOKIE_SECURE`: A boolean that determines whether the session cookie should be sent only over HTTPS. **Default:** `True` if `DEBUG` is `False`, `False` otherwise. **Should be `True` in production.**

## Databases

Database connection settings are configured via the `DATABASE_URL` environment variable.

```python
DJANGO_DATABASE_URL = env.db("DATABASE_URL")
DATABASES = {"default": DJANGO_DATABASE_URL}
```

*   `DJANGO_DATABASE_URL`: The database connection string, parsed by `django-environ`. **Default:** Loaded from the `DATABASE_URL` environment variable.
*   `DATABASES`: A dictionary containing the database configurations. The `default` key holds the primary database connection.
*   `DEFAULT_AUTO_FIELD`: The type of primary key to use for models that don't explicitly specify one. **Default:** `django.db.models.BigAutoField`. This uses a 64-bit integer, which is generally preferred over `AutoField` (32-bit) to avoid overflow issues in large applications.

## Applications Configuration

This section lists all installed Django applications and middleware.

*   `INSTALLED_APPS`: A list of strings designating all applications that are enabled in this Django installation. **Default:** Includes Django's built-in apps (admin, auth, contenttypes, sessions, messages, staticfiles), third-party libraries (whitenoise, corsheaders, rest_framework, django_filters, knox, django_celery_beat, django_celery_results, drf_spectacular, django_extensions), and local project apps (apps.users, apps.core). This setting tells Django which applications are active in your project.

*   `MIDDLEWARE`: A list of middleware classes to use. Middleware components process requests and responses globally. **Default:** Includes security, static files, session, CORS, common, CSRF, authentication, custom `RequestIDMiddleware`, and messages middleware. The order of middleware is important as they are processed in the order they appear in this list.

## Templates

Configuration for Django's template engine.

*   `BACKEND`: The template engine to use. **Default:** `django.template.backends.django.DjangoTemplates`.
*   `DIRS`: A list of directories where Django should look for template files. **Default:** `[root_path("templates")]`. This allows you to place project-wide templates outside of specific app directories.
*   `APP_DIRS`: A boolean that tells Django to look for templates inside the `templates` subdirectory of installed applications. **Default:** `True`. This is a convenient way to organize app-specific templates.
*   `OPTIONS`: A dictionary of options for the template engine. **Default:** Includes `context_processors` (which add variables to the template context, such as `debug`, `request`, `auth`, `messages`) and `builtins` (which register built-in template tags and filters).

## REST Framework

Settings for Django REST Framework (DRF) and related authentication/API schema tools.

### `REST_KNOX`

Configuration for `django-rest-knox`, the token-based authentication system.

*   `SECURE_HASH_ALGORITHM`: The hashing algorithm used for tokens. **Default:** `hashlib.sha512`.
*   `AUTH_TOKEN_CHARACTER_LENGTH`: The length of the authentication token. **Default:** `64`.
*   `TOKEN_TTL`: Token time-to-live. **Default:** `timedelta(hours=10)`. This defines how long a token is valid.
*   `USER_SERIALIZER`: The serializer used for user profiles. **Default:** `apps.users.serializers.UserProfileSerializer`.
*   `TOKEN_LIMIT_PER_USER`: Limits the number of active tokens per user. **Default:** `None` (no limit).
*   `AUTO_REFRESH`: Whether tokens should be automatically refreshed. **Default:** `False`.
*   `AUTO_REFRESH_MAX_TTL`: Maximum time-to-live for auto-refreshed tokens. **Default:** `None`.
*   `MIN_REFRESH_INTERVAL`: Minimum interval between token refreshes. **Default:** `60` seconds.
*   `AUTH_HEADER_PREFIX`: The prefix for the Authorization header. **Default:** `Bearer`.
*   `TOKEN_MODEL`: The token model used. **Default:** `knox.AuthToken`.

### `REST_FRAMEWORK`

General DRF settings.

*   `DEFAULT_AUTHENTICATION_CLASSES`: Defines authentication methods. **Default:** `knox.auth.TokenAuthentication`. In `DEBUG` mode, `SessionAuthentication` and `BasicAuthentication` are also added.
*   `DEFAULT_FILTER_BACKENDS`: Enables filtering, searching, and ordering capabilities. **Default:** `django_filters.rest_framework.DjangoFilterBackend`, `rest_framework.filters.SearchFilter`, `rest_framework.filters.OrderingFilter`.
*   `DEFAULT_RENDERER_CLASSES`: Specifies how API responses are rendered. **Default:** `rest_framework.renderers.JSONRenderer`. In `DEBUG` mode, `BrowsableAPIRenderer` is also added.
*   `DEFAULT_SCHEMA_CLASS`: Integrates `drf-spectacular` for OpenAPI schema generation. **Default:** `drf_spectacular.openapi.AutoSchema`.
*   `DEFAULT_THROTTLE_RATES`: Configures rate limiting for different user types. **Default:** `user: "1000/day"`, `anon: "100/day"`, `user_login: "5/minute"`. These can be adjusted based on your application's needs.

### `SPECTACULAR_SETTINGS`

Settings for `drf-spectacular`, used for generating OpenAPI 3 documentation.

*   `TITLE`: The title of your API documentation. **Default:** `Django Starter Template`.
*   `DESCRIPTION`: A description of your API. **Default:** `A comprehensive starting point for your new API with Django and DRF`.
*   `VERSION`: The version of your API. **Default:** `0.1.0`.
*   `SERVE_INCLUDE_SCHEMA`: Whether to include the schema endpoint in the generated documentation. **Default:** `False`. Set to `True` if you want the raw OpenAPI schema to be accessible.

### CORS Headers

*   `CORS_ALLOW_ALL_ORIGINS`: A boolean that allows all origins for CORS requests in debug mode. **Default:** `True` if `DEBUG` is `True`, `False` otherwise. **Should be `False` in production for security.**
*   `CORS_ALLOWED_ORIGINS`: A list of allowed origins for CORS requests when `CORS_ALLOW_ALL_ORIGINS` is `False`. **Default:** Loaded from the `CORS_ALLOWED_ORIGINS` environment variable.

## Cache

Configuration for caching, using Redis.

*   `CACHES`: Defines cache backends. **Default:** A dictionary with a `default` cache using `django_redis.cache.RedisCache`.
*   `LOCATION`: The connection URL for the Redis server. **Default:** `redis://redis:6379` (loaded from `env("REDIS_URL", default="redis://redis:6379")`).
*   `OPTIONS`: Additional options for the Redis client. **Default:** `{"CLIENT_CLASS": "django_redis.client.DefaultClient"}`.
*   `USER_AGENTS_CACHE`: The cache alias to use for user agent caching. **Default:** `default`.

## Celery

Settings for Celery, the asynchronous task queue.

*   `CELERY_BROKER_URL`: The URL for the Celery message broker. **Default:** `redis://redis:6379` (loaded from `env("CELERY_BROKER_URL", default="redis://redis:6379")`).
*   `CELERY_RESULT_BACKEND`: Where Celery task results are stored. **Default:** `django-db` (loaded from `env("CELERY_RESULT_BACKEND", default="django-db")`).
*   `CELERY_BEAT_SCHEDULER`: Specifies the scheduler for periodic tasks. **Default:** `django_celery_beat.schedulers.DatabaseScheduler`. This enables managing periodic tasks via the Django admin.
*   `CELERY_ACCEPT_CONTENT`: A list of accepted content types for tasks. **Default:** `["application/json"]`.
*   `CELERY_TASK_SERIALIZER`: The default serialization method for tasks. **Default:** `json`.
*   `CELERY_RESULT_SERIALIZER`: The default serialization method for task results. **Default:** `json`.
*   `CELERY_TIMEZONE`: The timezone for Celery. **Default:** `America/Santiago`.
*   `CELERY_RESULT_EXTENDED`: Whether to store extended result information. **Default:** `True`.

## Email

Email backend settings for sending emails.

*   `EMAIL_HOST`: The hostname of the SMTP server. **Default:** `smtp.gmail.com` (loaded from `env("EMAIL_HOST", default="smtp.gmail.com")`).
*   `EMAIL_USE_TLS`: Whether to use TLS (Transport Layer Security) for the connection. **Default:** `True` (loaded from `env.bool("EMAIL_USE_TLS", default=True)`).
*   `EMAIL_PORT`: The port number for the SMTP server. **Default:** `587` (loaded from `env.int("EMAIL_PORT", default=587)`).
*   `EMAIL_HOST_USER`: The username for the SMTP server. **Default:** `""` (loaded from `env("EMAIL_HOST_USER", default="")`).
*   `EMAIL_HOST_PASSWORD`: The password for the SMTP server. **Default:** `""` (loaded from `env("EMAIL_HOST_PASSWORD", default="")`).

## Sentry and Logging

While logging has its own dedicated documentation page, this section briefly covers Sentry integration.

*   `IGNORABLE_404_URLS`: A list of regular expressions for URLs that should not trigger 404 errors in logging/error reporting. **Default:** Includes patterns for common favicon and Apple touch icon requests.
*   `LOGGING`: Detailed logging configuration (refer to the [Logging System](logging.md) documentation for more).
*   `sentry_sdk.init()`: Initializes Sentry for error tracking and performance monitoring in production environments. **Default:** Initialized with `dsn`, `traces_sample_rate=1.0`, and `profiles_sample_rate=1.0` when `DEBUG` is `False`.

## Static & Media Files

Settings for serving static and user-uploaded media files.

*   `STORAGES`: Defines storage backends for default and static files. **Default:** `FileSystemStorage` for default and `whitenoise.storage.CompressedManifestStaticFilesStorage` for static files.
*   `STATIC_URL`: The URL to use when referring to static files located in `STATIC_ROOT`. **Default:** `/static/`.
*   `STATICFILES_DIRS`: A list of directories where Django will look for additional static files. **Default:** `[root_path("static")]`.
*   `STATIC_ROOT`: The absolute path to the directory where `collectstatic` will gather all static files for deployment. **Default:** A temporary directory if `DEBUG` is `True`, otherwise `static_root` within the project root.
*   `MEDIA_URL`: The URL that handles the media served from `MEDIA_ROOT`. **Default:** `/media/`.
*   `MEDIA_ROOT`: The absolute path to the directory where user-uploaded media files are stored. **Default:** `media_root` within the project root.
*   `ADMIN_MEDIA_PREFIX`: The URL prefix for admin media files. **Default:** `/static/admin/`.

## Django Debug Toolbar and Django Extensions

These tools are enabled only in `DEBUG` mode for development purposes.

*   `debug_toolbar`: Provides a customizable debug panel for Django projects. **Default:** Added to `INSTALLED_APPS` and `MIDDLEWARE` if `DEBUG` is `True`.
*   `INTERNAL_IPS`: A list of IP addresses that are considered "internal" for the Debug Toolbar. **Default:** `["127.0.0.1"]`.
*   `django_extensions`: Offers a collection of custom extensions for Django, including useful management commands. **Default:** Added to `INSTALLED_APPS` if `DEBUG` is `True`.

These settings are conditionally added to `INSTALLED_APPS` and `MIDDLEWARE` when `DEBUG` is `True`.