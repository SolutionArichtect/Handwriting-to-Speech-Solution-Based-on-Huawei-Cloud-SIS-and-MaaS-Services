@echo off
cd /d "%~dp0"

if not exist venv (
    echo Virtual environment not found. Please run run_service.bat first to set it up.
    pause
    exit /b
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Setting PYTHONPATH...
set PYTHONPATH=%CD%\huaweicloud-python-sdk-sis-1.8.5

echo Running pipeline test client...
echo This will process data/1.jpg by default.
python tests\pipeline_test.py

pause
