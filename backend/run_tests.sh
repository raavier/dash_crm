#!/bin/bash
# Dashboard CRM Backend - Test Runner (Linux/Mac)

echo "===================================="
echo "Dashboard CRM API - Running Tests"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run run.sh first to create the environment."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure your Databricks credentials."
    echo ""
    exit 1
fi

# Install test dependencies if needed
echo "Checking dependencies..."
pip install -q pytest pytest-asyncio httpx > /dev/null 2>&1

echo ""
echo "Running tests..."
echo ""

# Parse command line argument
if [ -z "$1" ]; then
    # Run all tests
    pytest -v
elif [ "$1" = "queries" ]; then
    # Run only query tests
    pytest tests/test_queries.py -v
elif [ "$1" = "service" ]; then
    # Run only service tests
    pytest tests/test_service.py -v
elif [ "$1" = "api" ]; then
    # Run only API tests
    pytest tests/test_api.py -v
elif [ "$1" = "verifications" ]; then
    # Run only total verifications test
    pytest tests/test_queries.py::TestVerificationsQuery::test_total_verifications_2025 -v -s
else
    # Run specific test
    pytest "$@" -v
fi

echo ""
echo "===================================="
echo "Tests completed!"
echo "===================================="
