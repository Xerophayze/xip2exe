@echo off
echo Installing dependencies for Self-Extracting EXE Creator...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages from requirements.txt...
pip install -r requirements.txt

echo.
echo Setup complete! You can now run the program with:
echo python main.py
echo.
pause
