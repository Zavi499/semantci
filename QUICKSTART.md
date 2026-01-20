# 🚀 Quick Start Guide

Get up and running with the Semantic Keyword Analysis Tool in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

## Step 1: Setup (First Time Only)

```bash
# Clone or navigate to the repository
cd semantci

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

## Step 2: Start the Server

### Option A: Using Quick Start Script (Recommended)

**Linux/Mac:**
```bash
./run_api.sh
```

**Windows:**
```bash
run_api.bat
```

### Option B: Manual Start

```bash
# Activate virtual environment first (if not already activated)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Start the server
python -m uvicorn api.main:app --reload
```

## Step 3: Open the Web Interface

Once the server starts, you'll see:

```
=========================================
🚀 Starting API Server...
=========================================

🌐 Web Interface: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs
📖 Alternative Docs: http://localhost:8000/redoc
```

**Open your browser to:** http://localhost:8000

## Using the Web Interface

### Analyze a Single Keyword

1. Type a keyword in the search box (e.g., "python programming")
2. Click **Analyze** or press Enter
3. View comprehensive results:
   - Entity information and classification
   - Salience and authority scores (0-100)
   - Semantic relevance and topic clusters
   - Interactive knowledge graph
   - Taxonomy and ontology
   - Schema.org markup

### Analyze Multiple Keywords (Batch)

1. Click the **Batch** tab
2. Enter keywords (one per line):
   ```
   python programming
   machine learning
   docker containers
   react framework
   seo optimization
   ```
3. Click **Analyze Batch**
4. View summary statistics and individual results
5. Click any result for detailed analysis

### View History

1. Click the **History** tab
2. See all previous analyses
3. Click any item to view full results

## Quick Examples

Try these example keywords:
- **python programming** - Programming language analysis
- **machine learning** - AI/ML topic analysis
- **react framework** - Web framework analysis
- **seo optimization** - Digital marketing analysis
- **docker containers** - DevOps technology analysis

## Common Commands

### Stop the Server
Press `Ctrl + C` in the terminal

### Restart the Server
```bash
# If using the script:
./run_api.sh

# If running manually:
python -m uvicorn api.main:app --reload
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Clear API Cache
Click the "Clear Cache" button in the web interface or:
```bash
curl -X DELETE http://localhost:8000/cache
```

## Using the API Directly

### Single Keyword Analysis

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "python programming"}'
```

### Batch Analysis

```bash
curl -X POST "http://localhost:8000/analyze/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["python", "react", "docker"],
    "parallel": true
  }'
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Using Python API

```python
from src.analyzer import KeywordAnalyzer

# Initialize
analyzer = KeywordAnalyzer()

# Analyze a keyword
result = analyzer.analyze("python programming")

# Access results
print(f"Entity: {result.entity}")
print(f"Type: {result.entity_type}")
print(f"Topic: {result.topic}")
print(f"Salience: {result.salience}/100")
print(f"Authority: {result.topical_authority}/100")
print(f"Search Intent: {result.search_intent}")

# Export to JSON
json_result = result.to_json()
print(json_result)
```

## Troubleshooting

### Port Already in Use

Change the port:
```bash
python -m uvicorn api.main:app --reload --port 8001
```

Then access at: http://localhost:8001

### API Not Responding

1. Check the server is running
2. Verify terminal shows "Application startup complete"
3. Check for error messages in terminal

### Dependencies Missing

Reinstall:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Web Interface Not Loading

1. Ensure server is running
2. Check browser console for errors (F12)
3. Try clearing browser cache
4. Access directly: http://localhost:8000/static/index.html

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [frontend/README.md](frontend/README.md) for web interface details
- Explore [examples/](examples/) for Python usage examples
- View API docs at http://localhost:8000/docs

## Need Help?

- Check the logs in the terminal where the server is running
- Review error messages in the browser console (F12)
- Ensure all prerequisites are installed
- Verify Python version: `python --version` (should be 3.8+)

## Performance Tips

- Enable caching for faster repeated analyses
- Use batch processing for multiple keywords
- Run in production mode with workers for better performance:
  ```bash
  uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
  ```

## Success!

You should now have:
- ✅ A running API server
- ✅ An accessible web interface
- ✅ Ability to analyze keywords
- ✅ Interactive visualizations
- ✅ Comprehensive semantic data

**Enjoy analyzing keywords!** 🎉
