@echo off
REM Dashboard CRM Backend - Test Runner (Windows)

echo ====================================
echo Dashboard CRM API - Running Tests
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run run.bat first to create the environment.
    pause
    exit /b 1
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

REM Install test dependencies if needed
echo Checking dependencies...
pip install -q pytest pytest-asyncio httpx > nul 2>&1

echo.
echo Running tests...
echo.

REM Parse command line argument
if "%1"=="" (
    REM Run all tests
    pytest -v
) else if "%1"=="queries" (
    REM Run only query tests
    pytest tests/test_queries.py -v
) else if "%1"=="service" (
    REM Run only service tests
    pytest tests/test_service.py -v
) else if "%1"=="api" (
    REM Run only API tests
    pytest tests/test_api.py -v
) else if "%1"=="verifications" (
    REM Run only total verifications test
    pytest tests/test_queries.py::TestVerificationsQuery::test_total_verifications_2025 -v -s
) else (
    REM Run specific test
    pytest %* -v
)

echo.
echo ====================================
echo Tests completed!
echo ====================================
pause
