.PHONY: help \
	build up down restart logs shell \
	test docker-test \
	lint docker-lint \
	format docker-format \
	run chat \
	clean

help:
	@echo "Development"
	@echo "  make test"
	@echo "  make lint"
	@echo "  make format"
	@echo "  make run          - Start the server locally"
	@echo "  make chat         - Open terminal chat client"
	@echo ""
	@echo "Docker"
	@echo "  make up"
	@echo "  make down"
	@echo "  make shell"

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

restart: down up

logs:
	docker compose logs -f

shell:
	docker compose exec api bash

test:
	uv run pytest

docker-test:
	docker compose exec api uv run pytest

lint:
	uv run ruff check .
	uv run mypy app

docker-lint:
	docker compose exec api uv run ruff check .
	docker compose exec api uv run mypy app

format:
	uv run ruff format .
	uv run ruff check . --fix

docker-format:
	docker compose exec api uv run ruff format .
	docker compose exec api uv run ruff check . --fix

clean:
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	uv run uvicorn app.main:app --reload --port 8000

chat:
	uv run python -m cli
