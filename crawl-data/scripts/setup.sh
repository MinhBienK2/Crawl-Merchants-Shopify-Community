#!/bin/bash
# Setup script for Linux/Mac

set -e

echo "🚀 Setting up Shopify Community Crawler..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "✅ uv is installed"

# Sync dependencies
echo "📥 Installing dependencies..."
uv sync

echo "✅ Setup completed!"
echo ""
echo "To run the crawler:"
echo "  uv run python main.py"
echo ""
echo "Or activate virtual environment:"
echo "  source .venv/bin/activate"
echo "  python main.py"

