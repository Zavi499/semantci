"""
Scoring Module
Calculates salience, authority, and other relevance scores
"""

import logging
from typing import Dict, List, Any
import math

logger = logging.getLogger(__name__)


class SalienceScorer:
    """
    Calculates various scoring metrics for keyword analysis
    """

    # Authority weights for different source types
    AUTHORITY_WEIGHTS = {
        'Official Documentation': 1.0,
        'Wikipedia': 0.9,
        'Academic Journals': 0.95,
        'Stack Overflow': 0.85,
        'GitHub': 0.8,
        'Industry Publications': 0.75,
        'Google': 0.9,
        'arXiv': 0.95,
        'MDN Web Docs': 0.9,
    }

    def __init__(self):
        """Initialize the scorer"""
        logger.info("Initializing SalienceScorer")

    def calculate_salience(self, keyword: str, entity_data: Dict[str, Any],
                          semantic_data: Dict[str, Any]) -> float:
        """
        Calculate salience score (importance/prominence)

        Args:
            keyword: The search keyword
            entity_data: Entity extraction data
            semantic_data: Semantic analysis data

        Returns:
            Salience score (0-100)
        """
        logger.info(f"Calculating salience for: {keyword}")

        # Initialize score components
        entity_score = self._score_entity_quality(entity_data)
        semantic_score = self._score_semantic_richness(semantic_data)
        specificity_score = self._score_keyword_specificity(keyword)
        relationship_score = self._score_relationships(entity_data)

        # Weighted average
        weights = {
            'entity': 0.3,
            'semantic': 0.25,
            'specificity': 0.25,
            'relationships': 0.2
        }

        salience = (
            entity_score * weights['entity'] +
            semantic_score * weights['semantic'] +
            specificity_score * weights['specificity'] +
            relationship_score * weights['relationships']
        )

        # Normalize to 0-100 scale
        salience = min(max(salience * 100, 0), 100)

        logger.info(f"Salience score for '{keyword}': {salience}")
        return salience

    def calculate_authority(self, keyword: str, entity_data: Dict[str, Any]) -> float:
        """
        Calculate topical authority score

        Args:
            keyword: The search keyword
            entity_data: Entity extraction data

        Returns:
            Authority score (0-100)
        """
        logger.info(f"Calculating authority for: {keyword}")

        # Score based on authority sources
        sources_score = self._score_authority_sources(entity_data.get('authority_sources', []))

        # Score based on entity type
        entity_type_score = self._score_entity_type_authority(entity_data.get('entity_type', ''))

        # Score based on named entities
        named_entities_score = self._score_named_entities(entity_data.get('named_entities', []))

        # Score based on taxonomy depth
        taxonomy_score = self._score_taxonomy_depth(entity_data.get('taxonomy', []))

        # Weighted combination
        authority = (
            sources_score * 0.4 +
            entity_type_score * 0.25 +
            named_entities_score * 0.2 +
            taxonomy_score * 0.15
        )

        # Normalize to 0-100 scale
        authority = min(max(authority * 100, 0), 100)

        logger.info(f"Authority score for '{keyword}': {authority}")
        return authority

    def _score_entity_quality(self, entity_data: Dict[str, Any]) -> float:
        """Score the quality of entity extraction"""
        score = 0.0

        # Has specific entity type (not "General Concept")
        if entity_data.get('entity_type', 'General Concept') != 'General Concept':
            score += 0.3

        # Has attributes
        attributes = entity_data.get('attributes', [])
        if attributes:
            score += min(len(attributes) * 0.1, 0.3)

        # Has relationships
        relationships = entity_data.get('relationships', [])
        if relationships:
            score += min(len(relationships) * 0.05, 0.2)

        # Has named entities
        if entity_data.get('named_entities'):
            score += 0.2

        return min(score, 1.0)

    def _score_semantic_richness(self, semantic_data: Dict[str, Any]) -> float:
        """Score the semantic richness of analysis"""
        score = 0.0

        # Has specific topic (not "General")
        if semantic_data.get('topic', 'General') != 'General':
            score += 0.3

        # Has semantic relevance terms
        semantic_relevance = semantic_data.get('semantic_relevance', [])
        if semantic_relevance:
            score += min(len(semantic_relevance) * 0.05, 0.3)

        # Has topic cluster
        topic_cluster = semantic_data.get('topic_cluster', [])
        if topic_cluster:
            score += min(len(topic_cluster) * 0.05, 0.2)

        # Has specific search intent
        if semantic_data.get('search_intent'):
            score += 0.2

        return min(score, 1.0)

    def _score_keyword_specificity(self, keyword: str) -> float:
        """Score how specific/targeted the keyword is"""
        score = 0.5  # Base score

        # Length-based scoring (longer keywords are often more specific)
        word_count = len(keyword.split())
        if word_count == 1:
            score += 0.0
        elif word_count == 2:
            score += 0.15
        elif word_count == 3:
            score += 0.25
        else:
            score += 0.3

        # Contains modifiers (best, top, how to, etc.)
        modifiers = ['best', 'top', 'how to', 'what is', 'guide', 'tutorial', 'vs']
        if any(mod in keyword.lower() for mod in modifiers):
            score += 0.15

        # Contains year or version numbers (indicates specificity)
        if any(char.isdigit() for char in keyword):
            score += 0.1

        return min(score, 1.0)

    def _score_relationships(self, entity_data: Dict[str, Any]) -> float:
        """Score based on relationship richness"""
        relationships = entity_data.get('relationships', [])

        if not relationships:
            return 0.3  # Base score

        # More relationships indicate better connectivity
        score = 0.3 + min(len(relationships) * 0.15, 0.7)

        return min(score, 1.0)

    def _score_authority_sources(self, sources: List[str]) -> float:
        """Score based on authority of sources"""
        if not sources:
            return 0.4  # Base score

        total_weight = 0.0
        for source in sources:
            # Check if source matches known high-authority sources
            for auth_source, weight in self.AUTHORITY_WEIGHTS.items():
                if auth_source.lower() in source.lower():
                    total_weight += weight
                    break
            else:
                # Unknown source gets medium weight
                total_weight += 0.5

        # Average weight
        avg_weight = total_weight / len(sources)
        return min(avg_weight, 1.0)

    def _score_entity_type_authority(self, entity_type: str) -> float:
        """Score based on entity type specificity"""
        # More specific entity types indicate higher authority
        if entity_type == 'General Concept':
            return 0.3

        specific_types = [
            'Programming Language', 'Framework', 'Technology',
            'Artificial Intelligence', 'Database', 'Cloud Platform'
        ]

        if entity_type in specific_types:
            return 0.9

        return 0.6  # Medium specificity

    def _score_named_entities(self, named_entities: List[str]) -> float:
        """Score based on presence of named entities"""
        if not named_entities:
            return 0.3

        # More named entities indicate more specific content
        score = 0.3 + min(len(named_entities) * 0.15, 0.7)
        return min(score, 1.0)

    def _score_taxonomy_depth(self, taxonomy: List[str]) -> float:
        """Score based on taxonomy depth and specificity"""
        if not taxonomy or len(taxonomy) <= 1:
            return 0.3

        # Deeper taxonomy indicates more structured knowledge
        depth_score = 0.3 + min(len(taxonomy) * 0.15, 0.7)
        return min(depth_score, 1.0)

    def calculate_relevance_score(self, keyword: str, target_keyword: str) -> float:
        """
        Calculate relevance score between two keywords

        Args:
            keyword: Source keyword
            target_keyword: Target keyword to compare

        Returns:
            Relevance score (0-100)
        """
        # Simple token overlap scoring
        keyword_tokens = set(keyword.lower().split())
        target_tokens = set(target_keyword.lower().split())

        if not keyword_tokens or not target_tokens:
            return 0.0

        # Jaccard similarity
        intersection = keyword_tokens.intersection(target_tokens)
        union = keyword_tokens.union(target_tokens)

        jaccard = len(intersection) / len(union) if union else 0.0

        # Scale to 0-100
        return round(jaccard * 100, 2)

    def calculate_trending_score(self, keyword: str) -> float:
        """
        Calculate a trending/popularity score (simplified version)

        Args:
            keyword: The search keyword

        Returns:
            Trending score (0-100)
        """
        # In a real implementation, this would use actual search volume data
        # For now, we'll use a heuristic based on keyword characteristics

        score = 50.0  # Base score

        # Trending indicators
        trending_terms = ['new', 'latest', '2024', '2025', '2026', 'modern', 'future']
        if any(term in keyword.lower() for term in trending_terms):
            score += 20

        # Popular technologies (simplified)
        popular_tech = ['ai', 'machine learning', 'react', 'python', 'cloud', 'docker']
        if any(tech in keyword.lower() for tech in popular_tech):
            score += 15

        # Commercial intent often indicates higher search volume
        commercial_terms = ['best', 'top', 'buy', 'review']
        if any(term in keyword.lower() for term in commercial_terms):
            score += 10

        return min(score, 100.0)
