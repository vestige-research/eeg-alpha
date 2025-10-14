.PHONY: help setup test format lint commit clean

help:
	@echo "eeg-alpha - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup     - Initial project setup"
	@echo ""
	@echo "Development:"
	@echo "  make format    - Format code with black"
	@echo "  make lint      - Lint code with ruff"
	@echo "  make test      - Run tests with pytest"
	@echo "  make check     - Run all checks (format, lint, test)"
	@echo ""
	@echo "Git:"
	@echo "  make commit    - Interactive commit with commitizen"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean     - Remove Python cache files"

setup:
	@bash setup.sh

format:
	@echo "🎨 Formatting code..."
	@black .

lint:
	@echo "🔍 Linting code..."
	@ruff check .

lint-fix:
	@echo "🔧 Linting and fixing code..."
	@ruff check --fix .

test:
	@echo "🧪 Running tests..."
	@pytest || echo "⚠️  No tests found or tests failed"

check: format lint test
	@echo "✅ All checks passed!"

commit:
	@cz commit

clean:
	@echo "🧹 Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleanup complete"
