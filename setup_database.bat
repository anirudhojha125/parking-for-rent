@echo off
title Smart Park System Database Setup

echo ==========================================
echo   Smart Park System Database Setup
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
echo Creating database and tables...
echo.

REM Run the Python script to create database and tables
python init_db.py

if %errorlevel% == 0 (
    echo.
    echo Database setup completed successfully!
    echo.
    echo Database name: smart_park_system
    echo Username: root
    echo Password: (empty)
    echo Port: 3306
) else (
    echo.
    echo ERROR: Failed to set up database.
    echo Please make sure:
    echo 1. XAMPP is installed
    echo 2. MySQL service is running
    echo 3. Python is installed and in PATH
)

echo.
echo Setup complete!
echo.
pause