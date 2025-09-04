#!/bin/bash
# Smart Video Splitter - GUI Launcher (Shell Script)
# For Unix/Linux/macOS users

echo "🚀 Launching Smart Video Splitter GUI..."
echo "📁 Project root: $(pwd)"
echo "⏳ Please wait..."

# Check if Python is available
if command -v python3 &> /dev/null; then
    python3 run.py
elif command -v python &> /dev/null; then
    python run.py
else
    echo "❌ Error: Python not found. Please install Python 3.6+ and try again."
    exit 1
fi
