@echo off
setlocal

:: Define the desired Python version
set PYTHON_VERSION_MAJOR=3
set PYTHON_VERSION_MINOR=10

set REQUIREMENTS_FILE=prod-requirements.txt

:: Define the virtual environment directory name
set VENV_DIR=venv

echo.
echo === Python Project Setup ===
echo.

:: 1. Check if 'py' launcher is installed
echo Checking for Python launcher ('py')...
where py >nul 2>&1
if %errorlevel% neq 0 (
    echo The 'py' launcher is not found in your PATH.
    echo This usually means Python is not installed or not added to PATH correctly.
    echo Attempting to open the Python %PYTHON_VERSION_MAJOR%.%PYTHON_VERSION_MINOR% download page...
    start "" "%PYTHON_INSTALLER_URL%"
    echo.
    echo IMPORTANT: Please download and install Python %PYTHON_VERSION_MAJOR%.%PYTHON_VERSION_MINOR% from the page that opened.
    echo Make sure to check the option "Add Python to PATH" during installation.
    echo After installation is complete, close this window and run the batch file again.
    echo Press any key to exit.
    pause
    goto end
)

echo 'py' launcher found.

:: 2. Create a virtual environment
if exist "%VENV_DIR%" (
    echo Virtual environment "%VENV_DIR%" already exists. Skipping creation.
) else (
    echo Creating virtual environment "%VENV_DIR%"...
    py -3.10 -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        echo Please ensure Python is correctly installed and accessible.
        echo Press any key to exit.
        pause
        goto end
    )
    echo Virtual environment created successfully.
)

echo.

:: 3. Activate the virtual environment and install requirements
echo Activating virtual environment and installing requirements from %REQUIREMENTS_FILE%...
if not exist %REQUIREMENTS_FILE% (
    echo Warning: %REQUIREMENTS_FILE% not found in the current directory.
    echo Skipping dependency installation.
    echo Make sure '%REQUIREMENTS_FILE%' is in the same directory as this batch file.
) else (
    call "%VENV_DIR%\Scripts\activate.bat"
    if %errorlevel% neq 0 (
        echo Error: Failed to activate virtual environment.
        echo Press any key to exit.
        pause
        goto end
    )
    pip install -r %REQUIREMENTS_FILE%
    if %errorlevel% neq 0 (
        echo Error: Failed to install all requirements.
        echo Please check the error messages above for details.
        echo Press any key to exit.
        pause
        goto end
    )
    echo All requirements installed successfully.
)

echo.
echo Setup complete!
echo To activate the virtual environment later, run: %VENV_DIR%\Scripts\activate.bat
echo You can then run your Python project.
echo Press any key to exit.
pause

:end
endlocal