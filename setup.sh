#!/bin/bash

# Video Editor Dependencies Setup Launcher for Unix-like systems
echo "================================================"
echo "Video Editor Dependencies Setup"
echo "================================================"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python is not installed or not in PATH"
    echo "Please install Python 3.7+ from https://python.org"
    echo "Or use your system's package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi

echo "✅ Python found: $($PYTHON_CMD --version)"
echo ""

# Run the setup script
echo "🚀 Starting dependency installation..."
$PYTHON_CMD setup_dependencies.py

echo ""
echo "Setup completed! Check the output above for any errors."


