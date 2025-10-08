.PHONY: help install test lint format typecheck clean docker-build docker-run docker-stop all

help:
	@echo "OpenGov-WaterfrontEngineering - Development Commands"
	@echo ""
	@echo "  make install        Install package and dependencies"
	@echo "  make test           Run test suite"
	@echo "  make test-cov       Run tests with coverage report"
	@echo "  make lint           Run linter (ruff)"
	@echo "  make format         Format code with ruff"
	@echo "  make typecheck      Run type checking with mypy"
	@echo "  make all            Format, lint, typecheck, and test"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run Docker container"
	@echo "  make docker-stop    Stop Docker container"
	@echo "  make clean          Clean up generated files"

install:
	pip install -e .

test:
	pytest -v

test-cov:
	pytest --cov=open_gov_waterfront --cov-report=term-missing --cov-report=html

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy src

all: format lint typecheck test

docker-build:
	docker build -t opengov-waterfront:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage dist/ build/
