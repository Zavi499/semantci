"""
FastAPI REST API for Keyword Analysis Tool
Provides endpoints for single and batch keyword analysis
"""

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
import logging
import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyzer import KeywordAnalyzer, KeywordAnalysisResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Semantic Keyword Analysis API",
    description="A comprehensive keyword analysis tool that extracts structured semantic data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer
analyzer = KeywordAnalyzer(use_cache=True, max_workers=4)

# Mount static files for frontend
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    logger.info(f"Frontend mounted at /static from {frontend_path}")


# Request/Response Models
class KeywordRequest(BaseModel):
    """Single keyword analysis request"""
    keyword: str = Field(..., description="The keyword to analyze", min_length=1, max_length=500)

    @validator('keyword')
    def validate_keyword(cls, v):
        if not v or not v.strip():
            raise ValueError('Keyword cannot be empty or whitespace')
        return v.strip()


class BatchKeywordRequest(BaseModel):
    """Batch keyword analysis request"""
    keywords: List[str] = Field(..., description="List of keywords to analyze", min_items=1, max_items=100)
    parallel: bool = Field(True, description="Process keywords in parallel")

    @validator('keywords')
    def validate_keywords(cls, v):
        if not v:
            raise ValueError('Keywords list cannot be empty')
        # Validate and clean each keyword
        cleaned = [kw.strip() for kw in v if kw and kw.strip()]
        if not cleaned:
            raise ValueError('No valid keywords provided')
        if len(cleaned) > 100:
            raise ValueError('Maximum 100 keywords allowed per batch')
        return cleaned


class AnalysisResponse(BaseModel):
    """Analysis response model"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class BatchAnalysisResponse(BaseModel):
    """Batch analysis response model"""
    success: bool
    processed: int
    results: Dict[str, Union[Dict[str, Any], Dict[str, str]]]
    errors: Optional[List[str]] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    cache_stats: Dict[str, Any]


# API Endpoints

@app.get("/")
async def root():
    """Serve the frontend application"""
    frontend_file = os.path.join(frontend_path, 'index.html')
    if os.path.exists(frontend_file):
        return FileResponse(frontend_file)
    return {
        "message": "Semantic Keyword Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "frontend": "/static/index.html"
    }

@app.get("/api", response_model=Dict[str, str])
async def api_info():
    """API information endpoint"""
    return {
        "message": "Semantic Keyword Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        cache_stats=analyzer.get_cache_stats()
    )


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_keyword(request: KeywordRequest):
    """
    Analyze a single keyword and return structured data

    **Request Body:**
    - keyword: The search term to analyze (required, 1-500 characters)

    **Response:**
    Returns comprehensive keyword analysis including:
    - Entity information and classification
    - Semantic analysis and search intent
    - Knowledge graph representation
    - Schema.org markup
    - Topical authority and salience scores
    - Related terms and topic clusters
    """
    try:
        logger.info(f"Analyzing keyword: {request.keyword}")
        result = analyzer.analyze(request.keyword)

        return AnalysisResponse(
            success=True,
            data=result.to_dict()
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/batch", response_model=BatchAnalysisResponse)
async def analyze_keywords_batch(request: BatchKeywordRequest):
    """
    Analyze multiple keywords in batch

    **Request Body:**
    - keywords: List of keywords to analyze (1-100 keywords)
    - parallel: Process in parallel (default: true)

    **Response:**
    Returns analysis results for all keywords with success/error status for each
    """
    try:
        logger.info(f"Batch analyzing {len(request.keywords)} keywords")
        results = analyzer.analyze_batch(request.keywords, parallel=request.parallel)

        # Separate successful results from errors
        processed = len(results)
        errors = []

        formatted_results = {}
        for keyword, result in results.items():
            if isinstance(result, KeywordAnalysisResult):
                formatted_results[keyword] = result.to_dict()
            else:
                # Error case
                formatted_results[keyword] = result
                errors.append(f"{keyword}: {result.get('error', 'Unknown error')}")

        return BatchAnalysisResponse(
            success=True,
            processed=processed,
            results=formatted_results,
            errors=errors if errors else None
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Batch analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")


@app.get("/analyze/{keyword}", response_model=AnalysisResponse)
async def analyze_keyword_get(keyword: str):
    """
    Analyze a keyword using GET request (for simple queries)

    **Path Parameter:**
    - keyword: The search term to analyze

    **Example:** `/analyze/python`
    """
    try:
        logger.info(f"GET analyzing keyword: {keyword}")

        # Validate keyword
        if not keyword or len(keyword.strip()) == 0:
            raise HTTPException(status_code=400, detail="Keyword cannot be empty")

        if len(keyword) > 500:
            raise HTTPException(status_code=400, detail="Keyword exceeds maximum length")

        result = analyzer.analyze(keyword.strip())

        return AnalysisResponse(
            success=True,
            data=result.to_dict()
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.delete("/cache", response_model=Dict[str, str])
async def clear_cache():
    """
    Clear the analysis cache

    **Response:**
    Returns confirmation message
    """
    try:
        analyzer.clear_cache()
        logger.info("Cache cleared")
        return {"message": "Cache cleared successfully", "status": "success"}

    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")


@app.get("/cache/stats", response_model=Dict[str, Any])
async def get_cache_stats():
    """
    Get cache statistics

    **Response:**
    Returns cache statistics including number of cached keywords
    """
    return analyzer.get_cache_stats()


# Error Handlers

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors"""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "validation_error"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "server_error"}
    )


# Startup/Shutdown Events

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Starting Semantic Keyword Analysis API")
    logger.info("API is ready to accept requests")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down Semantic Keyword Analysis API")
    analyzer.clear_cache()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
