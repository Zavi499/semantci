"""
Tests for the main KeywordAnalyzer class
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyzer import KeywordAnalyzer, KeywordAnalysisResult


class TestKeywordAnalyzer:
    """Test suite for KeywordAnalyzer"""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return KeywordAnalyzer(use_cache=False)

    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        analyzer = KeywordAnalyzer()
        assert analyzer is not None
        assert analyzer.use_cache is True
        assert analyzer.max_workers == 4

    def test_validate_keyword_valid(self, analyzer):
        """Test keyword validation with valid input"""
        is_valid, error = analyzer.validate_keyword("python programming")
        assert is_valid is True
        assert error is None

    def test_validate_keyword_empty(self, analyzer):
        """Test keyword validation with empty string"""
        is_valid, error = analyzer.validate_keyword("")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_validate_keyword_whitespace(self, analyzer):
        """Test keyword validation with whitespace"""
        is_valid, error = analyzer.validate_keyword("   ")
        assert is_valid is False
        assert "whitespace" in error.lower()

    def test_validate_keyword_too_long(self, analyzer):
        """Test keyword validation with too long string"""
        long_keyword = "a" * 501
        is_valid, error = analyzer.validate_keyword(long_keyword)
        assert is_valid is False
        assert "maximum length" in error.lower()

    def test_analyze_single_keyword(self, analyzer):
        """Test analyzing a single keyword"""
        result = analyzer.analyze("python")
        assert isinstance(result, KeywordAnalysisResult)
        assert result.entity is not None
        assert result.entity_type is not None
        assert result.salience >= 0
        assert result.salience <= 100
        assert result.topical_authority >= 0
        assert result.topical_authority <= 100

    def test_analyze_programming_keyword(self, analyzer):
        """Test analyzing a programming-related keyword"""
        result = analyzer.analyze("python programming")
        assert result.entity is not None
        assert "programming" in result.entity_type.lower() or "language" in result.entity_type.lower()
        assert len(result.attributes) > 0
        assert len(result.semantic_relevance) > 0

    def test_analyze_result_structure(self, analyzer):
        """Test that analysis result has all required fields"""
        result = analyzer.analyze("react")
        assert hasattr(result, 'entity')
        assert hasattr(result, 'entity_type')
        assert hasattr(result, 'attributes')
        assert hasattr(result, 'relationships')
        assert hasattr(result, 'context')
        assert hasattr(result, 'search_intent')
        assert hasattr(result, 'semantic_relevance')
        assert hasattr(result, 'topic')
        assert hasattr(result, 'topic_cluster')
        assert hasattr(result, 'topical_authority')
        assert hasattr(result, 'knowledge_graph')
        assert hasattr(result, 'ontology')
        assert hasattr(result, 'taxonomy')
        assert hasattr(result, 'named_entities')
        assert hasattr(result, 'entity_disambiguation')
        assert hasattr(result, 'salience')
        assert hasattr(result, 'schema')
        assert hasattr(result, 'entity_authority')
        assert hasattr(result, 'confidence_scores')

    def test_analyze_to_dict(self, analyzer):
        """Test converting result to dictionary"""
        result = analyzer.analyze("docker")
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert 'entity' in result_dict
        assert 'entity_type' in result_dict
        assert 'salience' in result_dict

    def test_analyze_to_json(self, analyzer):
        """Test converting result to JSON"""
        result = analyzer.analyze("kubernetes")
        json_str = result.to_json()
        assert isinstance(json_str, str)
        assert '"entity"' in json_str
        assert '"salience"' in json_str

    def test_analyze_batch(self, analyzer):
        """Test batch analysis"""
        keywords = ["python", "react", "docker"]
        results = analyzer.analyze_batch(keywords, parallel=False)
        assert len(results) == 3
        for keyword in keywords:
            assert keyword in results

    def test_analyze_batch_parallel(self, analyzer):
        """Test parallel batch analysis"""
        keywords = ["machine learning", "seo", "cloud"]
        results = analyzer.analyze_batch(keywords, parallel=True)
        assert len(results) == 3

    def test_cache_functionality(self):
        """Test caching works correctly"""
        analyzer = KeywordAnalyzer(use_cache=True)

        # First analysis
        result1 = analyzer.analyze("python")

        # Get cache stats
        stats = analyzer.get_cache_stats()
        assert stats['cached_keywords'] == 1

        # Second analysis (should be cached)
        result2 = analyzer.analyze("python")

        # Results should be identical
        assert result1.entity == result2.entity
        assert result1.salience == result2.salience

        # Clear cache
        analyzer.clear_cache()
        stats = analyzer.get_cache_stats()
        assert stats['cached_keywords'] == 0

    def test_invalid_keyword_raises_error(self, analyzer):
        """Test that invalid keyword raises ValueError"""
        with pytest.raises(ValueError):
            analyzer.analyze("")

        with pytest.raises(ValueError):
            analyzer.analyze("   ")

    def test_knowledge_graph_structure(self, analyzer):
        """Test knowledge graph has correct structure"""
        result = analyzer.analyze("python")
        kg = result.knowledge_graph
        assert 'nodes' in kg
        assert 'edges' in kg
        assert isinstance(kg['nodes'], list)
        assert isinstance(kg['edges'], list)
        assert len(kg['nodes']) > 0

    def test_schema_structure(self, analyzer):
        """Test schema has correct structure"""
        result = analyzer.analyze("react")
        schema = result.schema
        assert '@context' in schema
        assert '@type' in schema
        assert schema['@context'] == 'https://schema.org'

    def test_confidence_scores(self, analyzer):
        """Test confidence scores are present and valid"""
        result = analyzer.analyze("machine learning")
        assert result.confidence_scores is not None
        assert 'entity_extraction' in result.confidence_scores
        assert 'semantic_analysis' in result.confidence_scores
        assert 'overall' in result.confidence_scores
        assert 0 <= result.confidence_scores['overall'] <= 1


@pytest.mark.asyncio
async def test_analyze_async():
    """Test async analysis"""
    analyzer = KeywordAnalyzer()
    result = await analyzer.analyze_async("python")
    assert isinstance(result, KeywordAnalysisResult)
    assert result.entity is not None


@pytest.mark.asyncio
async def test_analyze_batch_async():
    """Test async batch analysis"""
    analyzer = KeywordAnalyzer()
    keywords = ["python", "react"]
    results = await analyzer.analyze_batch_async(keywords)
    assert len(results) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
