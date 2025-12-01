.PHONY: help up down build rebuild shell migrate makemigrations test test-cov logs logs-worker logs-beat superuser seed clean prune ps

# Default target - show help
help:
	@echo "Django Starter Template - Docker Compose Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Service Management:"
	@echo "  up              Start all services (db, redis, backend, worker, beat)"
	@echo "  down            Stop all services"
	@echo "  build           Build Docker image"
	@echo "  rebuild         Rebuild image and restart services"
	@echo "  ps              Show running containers"
	@echo ""
	@echo "Django Commands:"
	@echo "  shell           Open Django shell"
	@echo "  migrate         Run database migrations"
	@echo "  makemigrations  Create new migrations"
	@echo "  superuser       Create a superuser"
	@echo "  seed            Seed database (20 users + superuser)"
	@echo ""
	@echo "Testing & Debugging:"
	@echo "  test            Run all tests"
	@echo "  test-cov        Run tests with coverage report"
	@echo "  logs            View backend logs (follow mode)"
	@echo "  logs-worker     View Celery worker logs"
	@echo "  logs-beat       View Celery beat logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean           Stop services and remove volumes"
	@echo "  prune           Remove unused Docker resources"

# Service Management
up:
	docker compose up

down:
	docker compose down

build:
	docker compose build

rebuild:
	docker compose up --build

ps:
	docker compose ps

# Django Commands
shell:
	docker compose exec backend python manage.py shell

migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

superuser:
	docker compose exec backend python manage.py createsuperuser

seed:
	docker compose exec backend python manage.py seed --users 20 --superuser --clean

# Testing & Debugging
test:
	docker compose exec backend pytest

test-cov:
	docker compose exec backend pytest --cov

test-html:
	docker compose exec backend pytest --cov --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

logs:
	docker compose logs -f backend

logs-worker:
	docker compose logs -f worker

logs-beat:
	docker compose logs -f beat

logs-all:
	docker compose logs -f

# Maintenance
clean:
	docker compose down -v

prune:
	docker system prune -f
	docker volume prune -f
