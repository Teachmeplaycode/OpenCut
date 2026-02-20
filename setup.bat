@echo off
REM Setup script for OpenCut (Windows)

echo Setting up OpenCut...

REM Check Python version
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To run OpenCut:
echo   venv\Scripts\activate.bat
echo   python main.py
echo.
echo To build executable:
echo   python build.py
pause
