#!/bin/bash
# Start the Keyword Analysis API with Web Interface

echo "==========================================="
echo "Semantic Keyword Analysis Tool"
echo "==========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
python -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
fi

echo ""
echo "==========================================="
echo "🚀 Starting API Server..."
echo "==========================================="
echo ""
echo "🌐 Web Interface: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "📖 Alternative Docs: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo "==========================================="
echo ""

# Start the API
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
