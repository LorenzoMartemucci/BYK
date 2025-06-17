# Define the desired Python version
$PYTHON_VERSION_MAJOR = 3
$PYTHON_VERSION_MINOR = 10
$PYTHON_VERSION = "$PYTHON_VERSION_MAJOR.$PYTHON_VERSION_MINOR"

$REQUIREMENTS_FILE = "prod-requirements.txt"

# Define the virtual environment directory name
$VENV_DIR = "venv"

Write-Host ""
Write-Host "=== Python Project Setup ==="
Write-Host ""

# --- 1. Check if 'py' launcher is installed ---
Write-Host "Checking for Python launcher ('py')..."
# Use Get-Command to check if 'py' is available in the path
try {
    # Test-Path for 'py.exe' or 'py' command
    # Using where.exe for a more direct equivalent to batch's 'where'
    $pyPath = (where.exe py 2>$null).Trim()
    if (-not $pyPath) {
        throw "Python launcher 'py' not found."
    }
    Write-Host "'py' launcher found at: $pyPath"
}
catch {
    Write-Host "The 'py' launcher is not found in your PATH." -ForegroundColor Red
    Write-Host "This usually means Python is not installed or not added to PATH correctly." -ForegroundColor Yellow
    Write-Host "Attempting to open the Python $PYTHON_VERSION download page..."

    # URL for Python downloads (adjust if a more specific one is needed)
    $PYTHON_INSTALLER_URL = "https://www.python.org/downloads/release/python-$PYTHON_VERSION_MAJOR$PYTHON_VERSION_MINOR/"

    Write-Host ""
    Write-Host "IMPORTANT: Please download and install Python $PYTHON_VERSION from the page $PYTHON_INSTALLER_URL" -ForegroundColor Yellow
    Write-Host "Make sure to check the option 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host "After installation is complete, close this window and run the PowerShell script again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit."
    exit 1 # Exit with an error code
}

Write-Host ""

# --- 2. Create a virtual environment ---
if (Test-Path -Path $VENV_DIR -PathType Container) {
    Write-Host "Virtual environment '$VENV_DIR' already exists. Skipping creation."
}
else {
    Write-Host "Creating virtual environment '$VENV_DIR' for Python $PYTHON_VERSION..."
    try {
        # Use the specific Python version with py launcher
        py -"$PYTHON_VERSION" -m venv $VENV_DIR -ErrorAction Stop
        Write-Host "Virtual environment created successfully." -ForegroundColor Green
    }
    catch {
        Write-Host "Error: Failed to create virtual environment." -ForegroundColor Red
        Write-Host "Please ensure Python $PYTHON_VERSION is correctly installed and accessible." -ForegroundColor Yellow
        Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
        Read-Host "Press Enter to exit."
        exit 1
    }
}

Write-Host ""

# --- 3. Activate the virtual environment and install requirements ---
Write-Host "Activating virtual environment and installing requirements from '$REQUIREMENTS_FILE'..."

if (-not (Test-Path -Path $REQUIREMENTS_FILE)) {
    Write-Host "Warning: '$REQUIREMENTS_FILE' not found in the current directory." -ForegroundColor Yellow
    Write-Host "Skipping dependency installation." -ForegroundColor Yellow
    Write-Host "Make sure '$REQUIREMENTS_FILE' is in the same directory as this script." -ForegroundColor Yellow
}
else {
    $venvActivateScript = Join-Path $VENV_DIR "Scripts\Activate.ps1"

    if (-not (Test-Path -Path $venvActivateScript)) {
        Write-Host "Error: Virtual environment activation script not found: $venvActivateScript" -ForegroundColor Red
        Write-Host "Press Enter to exit."
        Read-Host
        exit 1
    }

    # Execute the activation script.
    # The '. .' (dot space dot) syntax sources the script, meaning its changes
    # (like setting the prompt and PATH) affect the current PowerShell session.
    . $venvActivateScript

    if ($LASTEXITCODE -ne 0) { # $LASTEXITCODE holds the exit code of the last native command
        Write-Host "Error: Failed to activate virtual environment." -ForegroundColor Red
        Read-Host "Press Enter to exit."
        exit 1
    }

    Write-Host "Virtual environment activated." -ForegroundColor Green

    Write-Host "Installing dependencies from '$REQUIREMENTS_FILE'..."
    try {
        pip install -r $REQUIREMENTS_FILE -ErrorAction Stop
        Write-Host "All requirements installed successfully." -ForegroundColor Green
    }
    catch {
        Write-Host "Error: Failed to install all requirements." -ForegroundColor Red
        Write-Host "Please check the error messages above for details." -ForegroundColor Yellow
        Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
        Read-Host "Press Enter to exit."
        exit 1
    }
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To activate the virtual environment later, run: .\\$VENV_DIR\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "You can then run your Python project." -ForegroundColor Cyan
Read-Host "Press Enter to exit."

# End of script