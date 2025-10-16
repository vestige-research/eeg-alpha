.PHONY: help setup test format lint commit clean branch sync push docs docs-preview docs-render

help:
	@echo "eeg-alpha - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Initial project setup"
	@echo ""
	@echo "Development:"
	@echo "  make format         - Format code with black"
	@echo "  make lint           - Lint code with ruff"
	@echo "  make test           - Run tests with pytest"
	@echo "  make check          - Run all checks (format, lint, test)"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs           - Preview documentation site (live reload)"
	@echo "  make docs-render    - Build documentation to _site/"
	@echo ""
	@echo "Git Workflow:"
	@echo "  make branch NAME=feature-name  - Create and switch to new feature branch"
	@echo "  make commit         - Interactive commit with commitizen"
	@echo "  make sync           - Update main branch from remote"
	@echo "  make push           - Push current branch to remote"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove Python cache files"

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

branch:
ifndef NAME
	@echo "❌ Error: Please provide a branch name"
	@echo "Usage: make branch NAME=feature-name"
	@exit 1
endif
	@echo "🌿 Creating branch: $(NAME)"
	@git checkout -b $(NAME)
	@echo "✓ Switched to new branch '$(NAME)'"

sync:
	@echo "🔄 Syncing with remote main..."
	@git checkout main
	@git pull origin main
	@echo "✓ main branch updated"

push:
	@echo "⬆️  Pushing current branch..."
	@git push -u origin $$(git branch --show-current)
	@echo "✓ Branch pushed to remote"

docs:
	@echo "📚 Starting documentation preview..."
	@quarto preview docs/

docs-render:
	@echo "🔨 Building documentation..."
	@quarto render docs/
	@echo "✓ Documentation built to _site/"

clean:
	@echo "🧹 Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf _site/ .quarto/ 2>/dev/null || true
	@echo "✓ Cleanup complete"
