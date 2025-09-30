#!/bin/bash
# Kush Framework - Launcher Script

cd "$(dirname "$0")"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Setup environment
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Check dependencies
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import colorama, cryptography, requests, yaml" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Create necessary directories
mkdir -p stagers downloads logs

# Run Kush Framework
echo "🚀 Starting Kush Framework v3.0 (Empire-inspired)..."
python3 main.py "$@"