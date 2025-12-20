@echo off
REM Dashboard CRM Backend - Startup Script (Windows)

echo ====================================
echo Dashboard CRM API - Starting Server
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your Databricks credentials.
    echo.
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt > nul 2>&1
echo.

REM Start the server
echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo Documentation: http://localhost:8000/docs
echo.
python main.py
