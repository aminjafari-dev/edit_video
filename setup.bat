@echo off
REM Video Editor Dependencies Setup Launcher for Windows
echo ================================================
echo Video Editor Dependencies Setup
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Run the setup script
echo 🚀 Starting dependency installation...
python setup_dependencies.py

echo.
echo Setup completed! Check the output above for any errors.
pause


