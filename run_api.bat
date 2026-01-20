@echo off
REM Start the Keyword Analysis API (Windows)

echo Starting Semantic Keyword Analysis API...
echo ==========================================

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run: python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Dependencies not installed!
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start the API
echo Starting API server on http://0.0.0.0:8000
echo API Documentation: http://localhost:8000/docs
echo ==========================================
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
