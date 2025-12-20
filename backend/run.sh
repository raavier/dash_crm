#!/bin/bash
# Dashboard CRM Backend - Startup Script (Linux/Mac)

echo "===================================="
echo "Dashboard CRM API - Starting Server"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python -m venv venv
    echo ""
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

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo ""

# Start the server
echo "Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "Documentation: http://localhost:8000/docs"
echo ""
python main.py
