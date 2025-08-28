# AI-Powered Password Cracker Simulator - PowerShell Startup
# ========================================================

Write-Host "🔐 AI-Powered Password Cracker Simulator - PowerShell Startup" -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Checking Python installation..." -ForegroundColor Yellow

# Try different Python commands
$pythonCmd = $null

try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found: python" -ForegroundColor Green
        $pythonCmd = "python"
    }
} catch {
    # Python not found
}

if (-not $pythonCmd) {
    try {
        $pythonVersion = py --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python found: py" -ForegroundColor Green
            $pythonCmd = "py"
        }
    } catch {
        # py not found
    }
}

if (-not $pythonCmd) {
    try {
        $pythonVersion = python3 --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python found: python3" -ForegroundColor Green
            $pythonCmd = "python3"
        }
    } catch {
        # python3 not found
    }
}

if (-not $pythonCmd) {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    Write-Host "Or add Python to your system PATH" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting application with $pythonCmd..." -ForegroundColor Green
Write-Host ""

# Check if requirements are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    $null = & $pythonCmd -c "import flask" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Flask found" -ForegroundColor Green
    } else {
        Write-Host "❌ Flask not found. Installing requirements..." -ForegroundColor Red
        & $pythonCmd -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to install requirements" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
} catch {
    Write-Host "❌ Error checking dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Dependencies OK" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Starting web application..." -ForegroundColor Green
Write-Host "📱 Open http://localhost:5000 in your browser" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the application
& $pythonCmd start.py

Write-Host ""
Read-Host "Press Enter to exit"
