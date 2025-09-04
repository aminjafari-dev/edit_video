@echo off
REM Smart Video Splitter - GUI Launcher (Batch Script)
REM For Windows users

echo 🚀 Launching Smart Video Splitter GUI...
echo 📁 Project root: %CD%
echo ⏳ Please wait...

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python run.py
) else (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        python3 run.py
    ) else (
        echo ❌ Error: Python not found. Please install Python 3.6+ and try again.
        pause
        exit /b 1
    )
)

pause
