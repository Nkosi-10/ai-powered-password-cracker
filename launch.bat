@echo off
title AI-Powered Password Cracker Simulator
color 0A

echo.
echo ========================================
echo   AI-Powered Password Cracker Simulator
echo ========================================
echo.

echo Checking Python installation...
echo.

REM Try different Python commands
set PYTHON_CMD=

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found: python
    set PYTHON_CMD=python
    goto :found_python
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found: py
    set PYTHON_CMD=py
    goto :found_python
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found: python3
    set PYTHON_CMD=python3
    goto :found_python
)

echo [ERROR] Python not found!
echo.
echo Please install Python 3.8+ from https://python.org
echo Make sure to check "Add Python to PATH" during installation
echo.
pause
exit /b 1

:found_python
echo.
echo Starting application with %PYTHON_CMD%...
echo.

REM Check if requirements are installed
echo Checking dependencies...
%PYTHON_CMD% -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing requirements...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install requirements
        pause
        exit /b 1
    )
)

echo [OK] Dependencies ready
echo.
echo Starting web application...
echo.
echo [INFO] Open http://localhost:5000 in your browser
echo [INFO] Press Ctrl+C to stop the server
echo.

%PYTHON_CMD% app.py

echo.
echo Application stopped.
pause
