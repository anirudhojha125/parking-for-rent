@echo off
title Smart Park System Launcher

echo ==========================================
echo   Smart Park System - Main Launcher
echo ==========================================
echo.

:menu
echo Please select an option:
echo.
echo 1. Install Dependencies
echo 2. Set Up Database
echo 3. Start Application
echo 4. Read Setup Guide
echo 5. Exit
echo.
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" goto install_deps
if "%choice%"=="2" goto setup_db
if "%choice%"=="3" goto start_app
if "%choice%"=="4" goto read_guide
if "%choice%"=="5" goto exit
echo.
echo Invalid choice. Please try again.
echo.
pause
cls
goto menu

:install_deps
cls
echo Installing dependencies...
echo.
call install_dependencies.bat
echo.
pause
cls
goto menu

:setup_db
cls
echo Setting up database...
echo.
call setup_database.bat
echo.
pause
cls
goto menu

:start_app
cls
echo Starting application...
echo.
call start_app.bat
goto exit

:read_guide
cls
echo Opening setup guide...
echo.
if exist "SETUP_GUIDE.md" (
    start "" "SETUP_GUIDE.md"
) else (
    echo SETUP_GUIDE.md not found!
)
echo.
pause
cls
goto menu

:exit
echo.
echo Thank you for using Smart Park System!
echo.
pause
exit