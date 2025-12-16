#!/bin/bash
# Quick installation script for Imagen CLI

set -e

echo "🖼️  Installing Imagen CLI..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV not found. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✓ UV installed"
fi

# Navigate to script directory
cd "$(dirname "$0")"

echo "📦 Installing dependencies..."
uv sync

echo "🔧 Installing genimg command..."
uv pip install -e .

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Get your Google AI API key from: https://makersuite.google.com/app/apikey"
echo "2. Set it as an environment variable:"
echo "   export GOOGLE_AI_API_KEY=\"your-key-here\""
echo ""
echo "3. Test it:"
echo "   genimg \"a beautiful sunset\" --ask"
echo ""
echo "For more details, see README.md"
