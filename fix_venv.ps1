# PowerShell Script to Fix Virtual Environment on Windows with OneDrive
# Run this script in PowerShell as Administrator if you encounter permission issues

Write-Host "🔧 Starting Virtual Environment Fix Script..." -ForegroundColor Green
Write-Host "📁 Current Directory: $(Get-Location)" -ForegroundColor Yellow

# Step 1: Handle OneDrive Permission Issues
Write-Host "`n1️⃣ Checking OneDrive sync status..." -ForegroundColor Cyan
$currentPath = Get-Location
if ($currentPath -like "*OneDrive*") {
    Write-Host "⚠️  OneDrive folder detected. This may cause permission issues." -ForegroundColor Yellow
    Write-Host "💡 Recommendation: Consider moving project to C:\Dev\ or similar local folder" -ForegroundColor Yellow
    Write-Host "🔄 Continuing with OneDrive-safe commands..." -ForegroundColor Yellow
}

# Step 2: Delete broken virtual environment
Write-Host "`n2️⃣ Removing existing virtual environment..." -ForegroundColor Cyan
if (Test-Path ".venv") {
    Write-Host "🗑️  Found existing .venv folder, removing..." -ForegroundColor Yellow
    try {
        # Force remove with all subdirectories and files
        Remove-Item -Path ".venv" -Recurse -Force -ErrorAction Stop
        Write-Host "✅ Successfully removed .venv folder" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to remove .venv: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "🔧 Trying alternative removal method..." -ForegroundColor Yellow
        
        # Alternative method using cmd
        cmd /c "rmdir /s /q .venv" 2>$null
        
        if (-not (Test-Path ".venv")) {
            Write-Host "✅ Successfully removed .venv folder using cmd" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Manual removal required. Please delete .venv folder manually" -ForegroundColor Red
        }
    }
} else {
    Write-Host "ℹ️  No existing .venv folder found" -ForegroundColor Blue
}

# Step 3: Check Python installation
Write-Host "`n3️⃣ Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python not found in PATH. Please install Python first." -ForegroundColor Red
    exit 1
}

# Step 4: Create new virtual environment
Write-Host "`n4️⃣ Creating new virtual environment..." -ForegroundColor Cyan
try {
    # Use python -m venv for better compatibility
    python -m venv .venv --clear
    Write-Host "✅ Virtual environment created successfully" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to create virtual environment: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔧 Trying with py launcher..." -ForegroundColor Yellow
    
    try {
        py -m venv .venv --clear
        Write-Host "✅ Virtual environment created with py launcher" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed with py launcher as well. Check Python installation." -ForegroundColor Red
        exit 1
    }
}

# Step 5: Activate virtual environment
Write-Host "`n5️⃣ Activating virtual environment..." -ForegroundColor Cyan
$activateScript = ".\.venv\Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    try {
        # Check execution policy
        $executionPolicy = Get-ExecutionPolicy
        if ($executionPolicy -eq "Restricted") {
            Write-Host "⚠️  PowerShell execution policy is Restricted" -ForegroundColor Yellow
            Write-Host "🔧 Setting execution policy for current session..." -ForegroundColor Yellow
            Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
        }
        
        # Activate the virtual environment
        & $activateScript
        Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to activate: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "🔧 Trying alternative activation..." -ForegroundColor Yellow
        
        # Alternative activation using cmd
        cmd /c ".venv\Scripts\activate.bat && echo Virtual environment activated"
    }
} else {
    Write-Host "❌ Activation script not found at $activateScript" -ForegroundColor Red
    exit 1
}

# Step 6: Upgrade pip
Write-Host "`n6️⃣ Upgrading pip..." -ForegroundColor Cyan
try {
    python -m pip install --upgrade pip --no-warn-script-location
    Write-Host "✅ Pip upgraded successfully" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to upgrade pip: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔧 Continuing anyway..." -ForegroundColor Yellow
}

# Step 7: Install requirements
Write-Host "`n7️⃣ Installing requirements..." -ForegroundColor Cyan
if (Test-Path "requirements.txt") {
    try {
        Write-Host "📦 Installing packages from requirements.txt..." -ForegroundColor Blue
        python -m pip install -r requirements.txt --no-warn-script-location
        Write-Host "✅ All requirements installed successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to install some requirements: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "🔧 Trying with --user flag..." -ForegroundColor Yellow
        python -m pip install -r requirements.txt --user --no-warn-script-location
    }
} else {
    Write-Host "⚠️  requirements.txt not found in current directory" -ForegroundColor Yellow
    Write-Host "📁 Available files:" -ForegroundColor Blue
    Get-ChildItem -Name "*.txt" | ForEach-Object { Write-Host "   - $_" -ForegroundColor Gray }
}

# Step 8: Verify installation
Write-Host "`n8️⃣ Verifying installation..." -ForegroundColor Cyan
try {
    $pipList = python -m pip list --format=columns
    Write-Host "✅ Installed packages:" -ForegroundColor Green
    Write-Host $pipList -ForegroundColor Gray
}
catch {
    Write-Host "⚠️  Could not list installed packages" -ForegroundColor Yellow
}

# Final status
Write-Host "`n🎉 Virtual Environment Setup Complete!" -ForegroundColor Green
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "   ✅ Virtual environment created in .venv/" -ForegroundColor White
Write-Host "   ✅ Virtual environment activated" -ForegroundColor White
Write-Host "   ✅ Pip upgraded to latest version" -ForegroundColor White
Write-Host "   ✅ Requirements installed" -ForegroundColor White

Write-Host "`n🚀 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. To activate venv in future sessions: .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   2. To deactivate: deactivate" -ForegroundColor White
Write-Host "   3. To run your app: python app.py" -ForegroundColor White

Write-Host "`n💡 Troubleshooting:" -ForegroundColor Cyan
Write-Host "   - If activation fails: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor White
Write-Host "   - If OneDrive issues persist: Move project to C:\Dev\" -ForegroundColor White
Write-Host "   - Run PowerShell as Administrator if permission errors occur" -ForegroundColor White
