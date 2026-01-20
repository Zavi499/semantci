"""
Tests for FastAPI endpoints
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test suite for API endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "cache_stats" in data

    def test_analyze_post_valid(self):
        """Test POST analyze with valid keyword"""
        response = client.post(
            "/analyze",
            json={"keyword": "python"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "entity" in data["data"]

    def test_analyze_post_empty_keyword(self):
        """Test POST analyze with empty keyword"""
        response = client.post(
            "/analyze",
            json={"keyword": ""}
        )
        assert response.status_code == 422  # Validation error

    def test_analyze_post_whitespace(self):
        """Test POST analyze with whitespace keyword"""
        response = client.post(
            "/analyze",
            json={"keyword": "   "}
        )
        assert response.status_code == 422  # Validation error

    def test_analyze_get_valid(self):
        """Test GET analyze with valid keyword"""
        response = client.get("/analyze/python")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_analyze_get_with_spaces(self):
        """Test GET analyze with keyword containing spaces"""
        response = client.get("/analyze/python%20programming")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_analyze_batch_valid(self):
        """Test batch analyze with valid keywords"""
        response = client.post(
            "/analyze/batch",
            json={
                "keywords": ["python", "react", "docker"],
                "parallel": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["processed"] == 3
        assert "results" in data

    def test_analyze_batch_single_keyword(self):
        """Test batch analyze with single keyword"""
        response = client.post(
            "/analyze/batch",
            json={
                "keywords": ["python"],
                "parallel": False
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["processed"] == 1

    def test_analyze_batch_empty_list(self):
        """Test batch analyze with empty list"""
        response = client.post(
            "/analyze/batch",
            json={
                "keywords": [],
                "parallel": True
            }
        )
        assert response.status_code == 422  # Validation error

    def test_analyze_batch_too_many(self):
        """Test batch analyze with too many keywords"""
        keywords = [f"keyword{i}" for i in range(101)]
        response = client.post(
            "/analyze/batch",
            json={
                "keywords": keywords,
                "parallel": True
            }
        )
        assert response.status_code == 422  # Validation error

    def test_cache_stats(self):
        """Test cache stats endpoint"""
        response = client.get("/cache/stats")
        assert response.status_code == 200
        data = response.json()
        assert "cached_keywords" in data
        assert "cache_enabled" in data

    def test_clear_cache(self):
        """Test clear cache endpoint"""
        # First, analyze something to populate cache
        client.post("/analyze", json={"keyword": "test"})

        # Clear cache
        response = client.delete("/cache")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

        # Verify cache is cleared
        stats = client.get("/cache/stats").json()
        assert stats["cached_keywords"] == 0

    def test_analyze_response_structure(self):
        """Test that analyze response has correct structure"""
        response = client.post(
            "/analyze",
            json={"keyword": "machine learning"}
        )
        assert response.status_code == 200
        data = response.json()

        # Check top-level structure
        assert "success" in data
        assert "data" in data

        # Check data structure
        result = data["data"]
        required_fields = [
            "entity", "entity_type", "attributes", "relationships",
            "context", "search_intent", "semantic_relevance", "topic",
            "topic_cluster", "topical_authority", "knowledge_graph",
            "ontology", "taxonomy", "named_entities", "entity_disambiguation",
            "salience", "schema", "entity_authority", "confidence_scores"
        ]

        for field in required_fields:
            assert field in result, f"Missing field: {field}"

    def test_batch_response_structure(self):
        """Test that batch response has correct structure"""
        response = client.post(
            "/analyze/batch",
            json={"keywords": ["python", "react"]}
        )
        assert response.status_code == 200
        data = response.json()

        assert "success" in data
        assert "processed" in data
        assert "results" in data
        assert len(data["results"]) == 2

    def test_cors_headers(self):
        """Test that CORS headers are present"""
        response = client.options("/analyze")
        assert "access-control-allow-origin" in response.headers

    def test_docs_available(self):
        """Test that API docs are available"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_available(self):
        """Test that ReDoc is available"""
        response = client.get("/redoc")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
