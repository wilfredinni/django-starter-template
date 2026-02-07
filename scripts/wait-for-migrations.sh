#!/bin/sh
# Wait for database migrations to complete before starting Celery services

MAX_RETRIES=${MAX_RETRIES:-60}
SLEEP_SECONDS=${SLEEP_SECONDS:-2}
attempts=0

echo "Waiting for database to be ready..."
until python manage.py migrate --check > /dev/null 2>&1; do
    attempts=$((attempts + 1))
    if [ "$attempts" -ge "$MAX_RETRIES" ]; then
        echo "Migrations not ready after $attempts attempts, exiting."
        exit 1
    fi
    echo "Migrations not ready, waiting..."
    sleep "$SLEEP_SECONDS"
done

echo "Database migrations are ready!"
exec "$@"
