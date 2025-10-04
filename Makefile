.PHONY: help build up down restart logs shell test migrate makemigrations createsuperuser test-data clean

help:
	@echo "Available commands:"
	@echo "  make build          - Build Docker containers"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make logs           - View logs"
	@echo "  make shell          - Access Django shell"
	@echo "  make test           - Run tests"
	@echo "  make migrate        - Run database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make createsuperuser - Create a superuser"
	@echo "  make test-data      - Create test data"
	@echo "  make clean          - Remove containers and volumes"

build:
	docker compose build

up:
	docker compose up -d
	@echo "Services started! Access the API at http://localhost:8000"

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f web

shell:
	docker compose exec web python manage.py shell

test:
	docker compose exec web pytest

test-coverage:
	docker compose exec web pytest --cov=. --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

createsuperuser:
	docker compose exec web python manage.py createsuperuser

test-data:
	docker compose exec web python scripts/create_test_data.py

clean:
	docker compose down -v
	@echo "All containers and volumes removed"
