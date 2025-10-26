.PHONY: help test test-fast test-v test-cov test-cov-html lint format check db-upgrade db-downgrade db-reset run clean install

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Descubre Boyacá Backend - Makefile Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# =============================================================================
# Testing
# =============================================================================

test: ## Run all tests in parallel (fast)
	@echo "$(BLUE)Running all tests in parallel...$(NC)"
	uv run pytest tests/ -n auto -q

test-fast: ## Run all tests in parallel with minimal output
	@echo "$(BLUE)Running tests (fast mode)...$(NC)"
	uv run pytest tests/ -n auto -q --tb=no

test-v: ## Run all tests in parallel with verbose output
	@echo "$(BLUE)Running tests (verbose)...$(NC)"
	uv run pytest tests/ -n auto -v

test-single: ## Run tests without parallelization
	@echo "$(BLUE)Running tests (single process)...$(NC)"
	uv run pytest tests/ -v

test-auth: ## Run only auth tests
	@echo "$(BLUE)Running auth tests...$(NC)"
	uv run pytest tests/domains/auth -n auto -v

test-restaurants: ## Run only restaurant tests
	@echo "$(BLUE)Running restaurant tests...$(NC)"
	uv run pytest tests/domains/restaurants -n auto -v

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	uv run pytest tests/ -n auto --cov --cov-report=term-missing

test-cov-html: ## Run tests with HTML coverage report
	@echo "$(BLUE)Running tests with HTML coverage...$(NC)"
	uv run pytest tests/ -n auto --cov --cov-report=html
	@echo "$(GREEN)Coverage report generated in htmlcov/index.html$(NC)"

test-watch: ## Run tests in watch mode (requires pytest-watch)
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	uv run ptw tests/ -- -n auto

# =============================================================================
# Code Quality
# =============================================================================

lint: ## Run linter (ruff check)
	@echo "$(BLUE)Running linter...$(NC)"
	uv run ruff check .

format: ## Format code (ruff format)
	@echo "$(BLUE)Formatting code...$(NC)"
	uv run ruff format .

format-check: ## Check if code is formatted
	@echo "$(BLUE)Checking code format...$(NC)"
	uv run ruff format --check .

check: lint format-check ## Run all code quality checks
	@echo "$(GREEN)All checks passed!$(NC)"

fix: ## Auto-fix linting issues
	@echo "$(BLUE)Auto-fixing linting issues...$(NC)"
	uv run ruff check --fix .
	uv run ruff format .

# =============================================================================
# Database
# =============================================================================

db-upgrade: ## Run database migrations (upgrade to head)
	@echo "$(BLUE)Running database migrations...$(NC)"
	uv run alembic upgrade head

db-downgrade: ## Rollback last database migration
	@echo "$(YELLOW)Rolling back last migration...$(NC)"
	uv run alembic downgrade -1

db-reset: ## Reset database (WARNING: deletes all data)
	@echo "$(RED)Resetting database (deleting local.db)...$(NC)"
	rm -f local.db
	uv run alembic upgrade head
	@echo "$(GREEN)Database reset complete!$(NC)"

db-revision: ## Create a new migration (usage: make db-revision msg="your message")
	@echo "$(BLUE)Creating new migration...$(NC)"
	uv run alembic revision -m "$(msg)"

db-current: ## Show current database revision
	@echo "$(BLUE)Current database revision:$(NC)"
	uv run alembic current

db-history: ## Show migration history
	@echo "$(BLUE)Migration history:$(NC)"
	uv run alembic history

# =============================================================================
# Development
# =============================================================================

run: ## Run the development server
	@echo "$(BLUE)Starting development server...$(NC)"
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Run the production server
	@echo "$(BLUE)Starting production server...$(NC)"
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

install: ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	uv sync --all-extras

install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing dev dependencies...$(NC)"
	uv sync --all-extras --dev

update: ## Update dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	uv lock --upgrade
	uv sync --all-extras

# =============================================================================
# Cleanup
# =============================================================================

clean: ## Clean up cache and temporary files
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-db: ## Remove local database
	@echo "$(YELLOW)Removing local.db...$(NC)"
	rm -f local.db

# =============================================================================
# CI/CD Simulation
# =============================================================================

ci: clean lint format-check test-cov ## Run all CI checks locally
	@echo "$(GREEN)All CI checks passed!$(NC)"

pre-commit: format lint test-fast ## Run pre-commit checks
	@echo "$(GREEN)Pre-commit checks passed!$(NC)"

# =============================================================================
# Utility
# =============================================================================

shell: ## Open Python shell with app context
	@echo "$(BLUE)Opening Python shell...$(NC)"
	uv run python

routes: ## Show all API routes
	@echo "$(BLUE)API Routes:$(NC)"
	uv run python -c "from app.main import app; from fastapi.routing import APIRoute; routes = [route for route in app.routes if isinstance(route, APIRoute)]; [print(f'{route.methods} {route.path}') for route in sorted(routes, key=lambda r: r.path)]"

info: ## Show project information
	@echo "$(BLUE)Project Information:$(NC)"
	@echo "Python version: $$(uv run python --version)"
	@echo "UV version: $$(uv --version)"
	@echo "Tests: $$(find tests -name 'test_*.py' | wc -l | tr -d ' ') files"
	@echo "App modules: $$(find app -name '*.py' | wc -l | tr -d ' ') files"

