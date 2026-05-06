# Makefile for VulnLab Scanner
# Usage: make <target>

.PHONY: help install dev-install test lint format clean build publish check

help:  ## Show this help message
	@echo "VulnLab Scanner - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt
	pip install -e .

dev-install:  ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -e ".[dev]"
	pre-commit install

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

lint:  ## Run linters
	flake8 app/ tests/ --max-line-length=127 --max-complexity=10

format:  ## Format code with black and isort
	black --line-length=127 app/ tests/
	isort --profile=black --line-length=127 app/ tests/

format-check:  ## Check code formatting
	black --check --line-length=127 app/ tests/
	isort --check --profile=black --line-length=127 app/ tests/

security:  ## Run security checks
	bandit -r app/ -x tests/ -ll

clean:  ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean  ## Build package
	python -m build

publish: build  ## Publish to PyPI (requires PYPI_API_TOKEN)
	twine upload dist/*

check: lint test  ## Run all checks (lint + test)

pre-commit:  ## Run pre-commit on all files
	pre-commit run --all-files

docs:  ## Build documentation (if using Sphinx)
	cd docs && make html

run:  ## Run scanner with example (requires URL)
	python -m app.main -u http://example.com --all

.PHONY: help install dev-install test lint format clean build publish check
