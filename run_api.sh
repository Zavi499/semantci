#!/bin/bash
# Start the Keyword Analysis API

echo "Starting Semantic Keyword Analysis API..."
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Dependencies not installed!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the API
echo "Starting API server on http://0.0.0.0:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "=========================================="
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
