@echo off
title Smart Park System - Starting Application

echo ==========================================
echo   Smart Park System Application Startup
echo ==========================================
echo.

REM Check if XAMPP is installed
if not exist "C:\xampp\xampp-control.exe" (
    echo ERROR: XAMPP not found at C:\xampp\
    echo Please install XAMPP first and try again.
    echo.
    pause
    exit /b
)

echo XAMPP found. Checking services...
echo.

echo Starting MySQL service...
net start mysql >nul 2>&1
if %errorlevel% == 0 (
    echo MySQL service started successfully.
) else (
    echo MySQL service is already running or failed to start.
    echo Please check XAMPP Control Panel to ensure MySQL is running.
)

echo.
echo Starting Smart Park System application...
echo.

REM Run the Flask application
python app.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start the application.
    echo Please make sure:
    echo 1. All dependencies are installed (run install.py first)
    echo 2. Database is set up (run setup_database.bat first)
    echo 3. XAMPP MySQL is running
)

echo.
pause