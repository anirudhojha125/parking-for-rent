@echo off
title Smart Park System - Installing Dependencies

echo ==========================================
echo   Smart Park System Dependency Installer
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found.
    echo Please install Python 3.7+ and try again.
    echo.
    pause
    exit /b
)

echo Python found. Installing dependencies...
echo.

REM Install Python dependencies
pip install -r requirements.txt

if %errorlevel% == 0 (
    echo.
    echo Dependencies installed successfully!
    echo.
    echo Next steps:
    echo 1. Run setup_database.bat to create the database
    echo 2. Run start_app.bat to start the application
) else (
    echo.
    echo ERROR: Failed to install dependencies.
    echo Please make sure you have internet connection and try again.
)

echo.
pause