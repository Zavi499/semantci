"""
Main Keyword Analysis Engine
Orchestrates all analysis components to provide comprehensive keyword insights
"""

import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json

from .entity_extractor import EntityExtractor
from .semantic_engine import SemanticEngine
from .knowledge_graph import KnowledgeGraphBuilder
from .schema_builder import SchemaBuilder
from .scorer import SalienceScorer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class KeywordAnalysisResult:
    """Structured result for keyword analysis"""
    entity: str
    entity_type: str
    attributes: List[str]
    relationships: List[Dict[str, str]]
    context: str
    search_intent: str
    semantic_relevance: List[str]
    topic: str
    topic_cluster: List[str]
    topical_authority: float
    knowledge_graph: Dict[str, Any]
    ontology: Dict[str, Any]
    taxonomy: List[str]
    named_entities: List[str]
    entity_disambiguation: List[str]
    salience: float
    schema: Dict[str, Any]
    entity_authority: List[str]
    confidence_scores: Optional[Dict[str, float]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class KeywordAnalyzer:
    """
    Main keyword analysis engine that coordinates all analysis components
    """

    def __init__(self, use_cache: bool = True, max_workers: int = 4):
        """
        Initialize the keyword analyzer

        Args:
            use_cache: Enable caching for repeated analyses
            max_workers: Maximum number of parallel workers
        """
        logger.info("Initializing KeywordAnalyzer")
        self.use_cache = use_cache
        self.max_workers = max_workers
        self.cache: Dict[str, KeywordAnalysisResult] = {}

        # Initialize analysis components
        self.entity_extractor = EntityExtractor()
        self.semantic_engine = SemanticEngine()
        self.kg_builder = KnowledgeGraphBuilder()
        self.schema_builder = SchemaBuilder()
        self.scorer = SalienceScorer()

        logger.info("KeywordAnalyzer initialized successfully")

    def validate_keyword(self, keyword: str) -> tuple[bool, Optional[str]]:
        """
        Validate input keyword

        Args:
            keyword: Input keyword to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not keyword:
            return False, "Keyword cannot be empty"

        if not isinstance(keyword, str):
            return False, f"Keyword must be a string, got {type(keyword)}"

        if len(keyword.strip()) == 0:
            return False, "Keyword cannot be only whitespace"

        if len(keyword) > 500:
            return False, "Keyword exceeds maximum length of 500 characters"

        return True, None

    def analyze(self, keyword: str) -> KeywordAnalysisResult:
        """
        Analyze a single keyword and return structured data

        Args:
            keyword: The search term to analyze

        Returns:
            KeywordAnalysisResult object with comprehensive analysis

        Raises:
            ValueError: If keyword validation fails
        """
        # Validate input
        is_valid, error_msg = self.validate_keyword(keyword)
        if not is_valid:
            logger.error(f"Keyword validation failed: {error_msg}")
            raise ValueError(error_msg)

        keyword = keyword.strip()

        # Check cache
        if self.use_cache and keyword in self.cache:
            logger.info(f"Returning cached result for: {keyword}")
            return self.cache[keyword]

        logger.info(f"Analyzing keyword: {keyword}")

        try:
            # Extract entities and named entities
            entity_data = self.entity_extractor.extract(keyword)

            # Perform semantic analysis
            semantic_data = self.semantic_engine.analyze(keyword)

            # Build knowledge graph
            kg_data = self.kg_builder.build(keyword, entity_data, semantic_data)

            # Generate schema markup
            schema_data = self.schema_builder.generate(keyword, entity_data)

            # Calculate scores
            salience_score = self.scorer.calculate_salience(keyword, entity_data, semantic_data)
            authority_score = self.scorer.calculate_authority(keyword, entity_data)

            # Build comprehensive result
            result = KeywordAnalysisResult(
                entity=entity_data.get('entity', keyword),
                entity_type=entity_data.get('entity_type', 'Unknown'),
                attributes=entity_data.get('attributes', []),
                relationships=entity_data.get('relationships', []),
                context=semantic_data.get('context', ''),
                search_intent=semantic_data.get('search_intent', ''),
                semantic_relevance=semantic_data.get('semantic_relevance', []),
                topic=semantic_data.get('topic', ''),
                topic_cluster=semantic_data.get('topic_cluster', []),
                topical_authority=round(authority_score, 2),
                knowledge_graph=kg_data,
                ontology=entity_data.get('ontology', {'hierarchy': [], 'parent_concepts': []}),
                taxonomy=entity_data.get('taxonomy', []),
                named_entities=entity_data.get('named_entities', []),
                entity_disambiguation=entity_data.get('disambiguations', []),
                salience=round(salience_score, 2),
                schema=schema_data,
                entity_authority=entity_data.get('authority_sources', []),
                confidence_scores={
                    'entity_extraction': entity_data.get('confidence', 0.0),
                    'semantic_analysis': semantic_data.get('confidence', 0.0),
                    'overall': round((entity_data.get('confidence', 0.0) + semantic_data.get('confidence', 0.0)) / 2, 2)
                }
            )

            # Cache the result
            if self.use_cache:
                self.cache[keyword] = result

            logger.info(f"Successfully analyzed keyword: {keyword}")
            return result

        except Exception as e:
            logger.error(f"Error analyzing keyword '{keyword}': {str(e)}", exc_info=True)
            raise

    def analyze_batch(self, keywords: List[str], parallel: bool = True) -> Dict[str, Union[KeywordAnalysisResult, Dict[str, str]]]:
        """
        Analyze multiple keywords in batch

        Args:
            keywords: List of keywords to analyze
            parallel: Whether to process in parallel

        Returns:
            Dictionary mapping keywords to their analysis results or errors
        """
        logger.info(f"Starting batch analysis of {len(keywords)} keywords")
        results = {}

        if parallel:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_keyword = {
                    executor.submit(self._safe_analyze, kw): kw
                    for kw in keywords
                }

                for future in future_to_keyword:
                    keyword = future_to_keyword[future]
                    try:
                        results[keyword] = future.result()
                    except Exception as e:
                        logger.error(f"Batch processing error for '{keyword}': {str(e)}")
                        results[keyword] = {"error": str(e), "keyword": keyword}
        else:
            for keyword in keywords:
                results[keyword] = self._safe_analyze(keyword)

        logger.info(f"Batch analysis completed: {len(results)} results")
        return results

    def _safe_analyze(self, keyword: str) -> Union[KeywordAnalysisResult, Dict[str, str]]:
        """
        Safely analyze a keyword, catching exceptions

        Args:
            keyword: Keyword to analyze

        Returns:
            Analysis result or error dictionary
        """
        try:
            return self.analyze(keyword)
        except Exception as e:
            logger.error(f"Error in safe analyze for '{keyword}': {str(e)}")
            return {"error": str(e), "keyword": keyword}

    async def analyze_async(self, keyword: str) -> KeywordAnalysisResult:
        """
        Asynchronously analyze a keyword

        Args:
            keyword: The search term to analyze

        Returns:
            KeywordAnalysisResult object
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.analyze, keyword)

    async def analyze_batch_async(self, keywords: List[str]) -> Dict[str, Union[KeywordAnalysisResult, Dict[str, str]]]:
        """
        Asynchronously analyze multiple keywords

        Args:
            keywords: List of keywords to analyze

        Returns:
            Dictionary mapping keywords to their analysis results
        """
        tasks = [self.analyze_async(keyword) for keyword in keywords]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            keyword: result if not isinstance(result, Exception) else {"error": str(result), "keyword": keyword}
            for keyword, result in zip(keywords, results)
        }

    def clear_cache(self):
        """Clear the analysis cache"""
        logger.info("Clearing analysis cache")
        self.cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            "cached_keywords": len(self.cache),
            "cache_enabled": self.use_cache
        }
