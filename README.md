# Semantic Keyword Analysis Tool

A comprehensive, production-ready keyword analysis engine that extracts structured semantic data from search terms. Built with Python, spaCy, and FastAPI for high-performance semantic analysis.

## Features

- **Entity Extraction**: Identifies core entities, types, attributes, and relationships
- **Semantic Analysis**: Detects search intent, context, and semantic relevance
- **Knowledge Graph**: Constructs graph representations with nodes and edges
- **Schema.org Markup**: Generates structured data for SEO
- **Scoring Metrics**: Calculates salience and topical authority scores
- **Batch Processing**: Analyze multiple keywords in parallel
- **RESTful API**: FastAPI-powered endpoints with automatic documentation
- **Caching**: Built-in caching for improved performance
- **Confidence Scores**: Provides confidence metrics for each analysis component

## Technology Stack

- **Language**: Python 3.8+
- **Framework**: FastAPI
- **NLP**: spaCy
- **API Server**: Uvicorn
- **Data Validation**: Pydantic

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/semantci.git
cd semantci
```

### Step 2: Create Virtual Environment

```bash
# On Linux/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

## Running the Application

### Option 1: Run API Server

Start the FastAPI server:

```bash
# From the project root directory
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Option 2: Use Python Module Directly

```python
from src.analyzer import KeywordAnalyzer

# Initialize analyzer
analyzer = KeywordAnalyzer()

# Analyze a keyword
result = analyzer.analyze("machine learning")

# Print results
print(result.to_json())
```

### Option 3: Run with Custom Configuration

```bash
# Custom host and port
uvicorn api.main:app --host 127.0.0.1 --port 5000

# Production mode (without reload)
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### 1. Analyze Single Keyword (POST)

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "python programming"}'
```

### 2. Analyze Single Keyword (GET)

```bash
curl "http://localhost:8000/analyze/python%20programming"
```

### 3. Batch Analysis

```bash
curl -X POST "http://localhost:8000/analyze/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["python", "react", "machine learning"],
    "parallel": true
  }'
```

### 4. Health Check

```bash
curl "http://localhost:8000/health"
```

### 5. Clear Cache

```bash
curl -X DELETE "http://localhost:8000/cache"
```

### 6. Cache Statistics

```bash
curl "http://localhost:8000/cache/stats"
```

## Output Format

The tool returns a comprehensive JSON object with the following structure:

```json
{
  "entity": "string - core concept/thing",
  "entity_type": "string - category/classification",
  "attributes": ["array of key properties"],
  "relationships": [{"entity": "string", "type": "string"}],
  "context": "string - usage scenarios and background",
  "search_intent": "string - why users search for this",
  "semantic_relevance": ["array of synonyms and related terms"],
  "topic": "string - primary subject area",
  "topic_cluster": ["array of related topics"],
  "topical_authority": "number 0-100 - credibility score",
  "knowledge_graph": {"nodes": [], "edges": []},
  "ontology": {"hierarchy": [], "parent_concepts": []},
  "taxonomy": ["array of classification levels"],
  "named_entities": ["array of specific instances"],
  "entity_disambiguation": ["array of alternative meanings"],
  "salience": "number 0-100 - importance score",
  "schema": {"@type": "string", "properties": {}},
  "entity_authority": ["array of authoritative sources"],
  "confidence_scores": {
    "entity_extraction": "number 0-1",
    "semantic_analysis": "number 0-1",
    "overall": "number 0-1"
  }
}
```

## Usage Examples

### Example 1: Python Script

```python
from src.analyzer import KeywordAnalyzer

# Initialize
analyzer = KeywordAnalyzer(use_cache=True, max_workers=4)

# Single analysis
result = analyzer.analyze("python programming")
print(f"Entity: {result.entity}")
print(f"Type: {result.entity_type}")
print(f"Topic: {result.topic}")
print(f"Search Intent: {result.search_intent}")
print(f"Salience Score: {result.salience}")
print(f"Authority Score: {result.topical_authority}")

# Batch analysis
keywords = ["python", "react", "seo", "docker"]
results = analyzer.analyze_batch(keywords, parallel=True)

for keyword, result in results.items():
    if hasattr(result, 'entity'):
        print(f"{keyword}: {result.entity_type} - Authority: {result.topical_authority}")
```

### Example 2: Async Processing

```python
import asyncio
from src.analyzer import KeywordAnalyzer

async def analyze_keywords():
    analyzer = KeywordAnalyzer()

    # Async single analysis
    result = await analyzer.analyze_async("machine learning")
    print(result.to_json())

    # Async batch analysis
    keywords = ["ai", "deep learning", "neural networks"]
    results = await analyzer.analyze_batch_async(keywords)

    for keyword, result in results.items():
        print(f"{keyword}: {result.salience}")

asyncio.run(analyze_keywords())
```

### Example 3: Using the API with Python Requests

```python
import requests

# Single keyword analysis
response = requests.post(
    "http://localhost:8000/analyze",
    json={"keyword": "react framework"}
)
data = response.json()
print(data['data']['entity_type'])

# Batch analysis
response = requests.post(
    "http://localhost:8000/analyze/batch",
    json={
        "keywords": ["python", "javascript", "go"],
        "parallel": True
    }
)
results = response.json()
print(f"Processed: {results['processed']} keywords")
```

## Project Structure

```
semantci/
├── src/                          # Core analysis modules
│   ├── __init__.py
│   ├── analyzer.py               # Main analysis orchestrator
│   ├── entity_extractor.py       # Entity extraction & NER
│   ├── semantic_engine.py        # Semantic analysis
│   ├── knowledge_graph.py        # Knowledge graph builder
│   ├── schema_builder.py         # Schema.org markup
│   └── scorer.py                 # Scoring algorithms
├── api/                          # FastAPI application
│   ├── __init__.py
│   └── main.py                   # API endpoints
├── examples/                     # Example scripts
│   ├── basic_usage.py
│   ├── batch_processing.py
│   └── api_client.py
├── tests/                        # Test suite
│   ├── test_analyzer.py
│   ├── test_entity_extractor.py
│   └── test_api.py
├── config/                       # Configuration files
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Analysis Configuration
CACHE_ENABLED=true
MAX_WORKERS=4
MAX_BATCH_SIZE=100

# Logging
LOG_LEVEL=INFO
```

### Custom Configuration

```python
from src.analyzer import KeywordAnalyzer

# Custom configuration
analyzer = KeywordAnalyzer(
    use_cache=True,      # Enable/disable caching
    max_workers=8        # Number of parallel workers
)
```

## Performance Optimization

### Tips for Best Performance

1. **Enable Caching**: Use `use_cache=True` for repeated analyses
2. **Parallel Processing**: Use batch processing with `parallel=True`
3. **Adjust Workers**: Set `max_workers` based on CPU cores
4. **Production Mode**: Run uvicorn with multiple workers

```bash
uvicorn api.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Benchmarks

- Single keyword analysis: ~50-200ms
- Batch processing (10 keywords): ~300-800ms (parallel)
- Cache hit: ~1-5ms

## Error Handling

The tool provides comprehensive error handling:

```python
from src.analyzer import KeywordAnalyzer

analyzer = KeywordAnalyzer()

try:
    result = analyzer.analyze("")
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Analysis error: {e}")
```

API errors return appropriate HTTP status codes:
- `400`: Bad Request (validation error)
- `500`: Internal Server Error

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py
```

## Troubleshooting

### spaCy Model Not Found

```bash
python -m spacy download en_core_web_sm
```

### Import Errors

Ensure you're running from the project root:

```bash
cd semantci
python -m uvicorn api.main:app --reload
```

### Port Already in Use

Change the port:

```bash
uvicorn api.main:app --port 8001
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/semantci/issues
- Documentation: http://localhost:8000/docs (when running)

## Roadmap

- [ ] Add support for multiple languages
- [ ] Integrate with external APIs (Google Trends, Wikipedia)
- [ ] Add machine learning models for better accuracy
- [ ] Implement database storage for analysis history
- [ ] Add export formats (CSV, Excel, PDF)
- [ ] Create web dashboard UI
- [ ] Add real-time streaming analysis

## Acknowledgments

- Built with [spaCy](https://spacy.io/) for NLP
- Powered by [FastAPI](https://fastapi.tiangolo.com/) for API
- Inspired by semantic search and knowledge graph technologies
