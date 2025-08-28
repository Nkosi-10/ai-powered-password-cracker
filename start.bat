@echo off
echo 🔐 AI-Powered Password Cracker Simulator - Windows Startup
echo ========================================================

echo.
echo Checking Python installation...

REM Try different Python commands
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python found: python
    set PYTHON_CMD=python
    goto :start_app
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python found: py
    set PYTHON_CMD=py
    goto :start_app
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python found: python3
    set PYTHON_CMD=python3
    goto :start_app
)

echo ❌ Python not found in PATH
echo.
echo Please install Python 3.8+ from https://python.org
echo Or add Python to your system PATH
echo.
pause
exit /b 1

:start_app
echo.
echo 🚀 Starting application with %PYTHON_CMD%...
echo.

REM Check if requirements are installed
echo Checking dependencies...
%PYTHON_CMD% -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Flask not found. Installing requirements...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
)

echo ✅ Dependencies OK
echo.
echo 🌐 Starting web application...
echo 📱 Open http://localhost:5000 in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

%PYTHON_CMD% start.py

pause
