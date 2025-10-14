#!/bin/bash
# Setup script for eeg-alpha development environment

set -e

echo "🚀 Setting up eeg-alpha development environment..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install dev dependencies
echo "🛠️  Installing dev dependencies..."
pip install black ruff pytest pre-commit commitizen

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install
pre-commit install --hook-type commit-msg

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "Available commands (see Makefile):"
echo "  make test      - Run tests"
echo "  make format    - Format code"
echo "  make lint      - Lint code"
echo "  make commit    - Interactive commit"
