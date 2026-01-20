"""
Entity Extraction Module
Extracts entities, entity types, attributes, and relationships from keywords
"""

import logging
import re
from typing import Dict, List, Any
import spacy
from spacy.cli import download
import os

logger = logging.getLogger(__name__)


class EntityExtractor:
    """
    Extracts and analyzes entities from keywords using NLP
    """

    # Entity type mapping for common patterns
    ENTITY_TYPE_PATTERNS = {
        r'\b(python|java|javascript|ruby|go|rust|c\+\+|php)\b': 'Programming Language',
        r'\b(aws|azure|gcp|google cloud|cloud)\b': 'Cloud Platform',
        r'\b(react|vue|angular|django|flask|spring)\b': 'Framework',
        r'\b(api|rest|graphql|sdk)\b': 'Technology',
        r'\b(seo|marketing|analytics)\b': 'Digital Marketing',
        r'\b(machine learning|ai|deep learning|nlp)\b': 'Artificial Intelligence',
        r'\b(database|sql|nosql|mongodb|postgresql)\b': 'Database',
        r'\b(docker|kubernetes|jenkins|ci/cd)\b': 'DevOps',
    }

    # Common taxonomy hierarchies
    TAXONOMY_MAPPINGS = {
        'python': ['Technology', 'Programming', 'Languages', 'Interpreted Languages'],
        'react': ['Technology', 'Web Development', 'Frontend', 'JavaScript Frameworks'],
        'machine learning': ['Technology', 'Artificial Intelligence', 'Machine Learning'],
        'seo': ['Digital Marketing', 'SEO', 'Search Optimization'],
        'docker': ['Technology', 'DevOps', 'Containerization'],
    }

    # Ontology hierarchies
    ONTOLOGY_HIERARCHIES = {
        'python': {
            'hierarchy': ['Language', 'High-level Language', 'Interpreted Language', 'Python'],
            'parent_concepts': ['Programming Language', 'Software Development', 'Technology']
        },
        'react': {
            'hierarchy': ['Library', 'UI Library', 'JavaScript Library', 'React'],
            'parent_concepts': ['Frontend Framework', 'Web Development', 'User Interface']
        },
        'machine learning': {
            'hierarchy': ['AI', 'Machine Learning', 'Supervised Learning'],
            'parent_concepts': ['Artificial Intelligence', 'Data Science', 'Computer Science']
        }
    }

    def __init__(self):
        """Initialize the entity extractor with spaCy model"""
        logger.info("Initializing EntityExtractor")
        self.nlp = self._load_spacy_model()
        logger.info("EntityExtractor initialized")

    def _load_spacy_model(self):
        """Load spaCy model, download if necessary"""
        try:
            return spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found, using fallback mode")
            # Return None to indicate fallback mode
            return None

    def extract(self, keyword: str) -> Dict[str, Any]:
        """
        Extract entity information from keyword

        Args:
            keyword: Input keyword

        Returns:
            Dictionary containing entity data
        """
        logger.info(f"Extracting entities from: {keyword}")

        keyword_lower = keyword.lower().strip()

        # Determine entity and entity type
        entity = self._extract_entity(keyword)
        entity_type = self._determine_entity_type(keyword_lower)

        # Extract attributes
        attributes = self._extract_attributes(keyword_lower, entity_type)

        # Extract relationships
        relationships = self._extract_relationships(keyword_lower)

        # Get taxonomy
        taxonomy = self._get_taxonomy(keyword_lower)

        # Get ontology
        ontology = self._get_ontology(keyword_lower)

        # Extract named entities
        named_entities = self._extract_named_entities(keyword)

        # Generate disambiguations
        disambiguations = self._generate_disambiguations(keyword_lower)

        # Get authority sources
        authority_sources = self._get_authority_sources(keyword_lower, entity_type)

        # Calculate confidence
        confidence = self._calculate_confidence(keyword, entity_type)

        result = {
            'entity': entity,
            'entity_type': entity_type,
            'attributes': attributes,
            'relationships': relationships,
            'taxonomy': taxonomy,
            'ontology': ontology,
            'named_entities': named_entities,
            'disambiguations': disambiguations,
            'authority_sources': authority_sources,
            'confidence': confidence
        }

        logger.info(f"Entity extraction completed for: {keyword}")
        return result

    def _extract_entity(self, keyword: str) -> str:
        """Extract the core entity from keyword"""
        if self.nlp:
            doc = self.nlp(keyword)
            # Try to find the main noun or noun phrase
            for chunk in doc.noun_chunks:
                return chunk.text
            # If no noun chunks, return the keyword itself
        return keyword.strip()

    def _determine_entity_type(self, keyword: str) -> str:
        """Determine the type/category of the entity"""
        # Check against patterns
        for pattern, entity_type in self.ENTITY_TYPE_PATTERNS.items():
            if re.search(pattern, keyword, re.IGNORECASE):
                return entity_type

        # Use spaCy if available
        if self.nlp:
            doc = self.nlp(keyword)
            if doc.ents:
                return doc.ents[0].label_

        # Default classification based on common terms
        if any(word in keyword for word in ['how', 'what', 'why', 'guide', 'tutorial']):
            return 'Educational Content'
        elif any(word in keyword for word in ['buy', 'price', 'cost', 'shop']):
            return 'Commercial'
        elif any(word in keyword for word in ['best', 'top', 'review']):
            return 'Comparative/Review'
        else:
            return 'General Concept'

    def _extract_attributes(self, keyword: str, entity_type: str) -> List[str]:
        """Extract key attributes/properties"""
        attributes = []

        # Extract adjectives if spaCy is available
        if self.nlp:
            doc = self.nlp(keyword)
            for token in doc:
                if token.pos_ == 'ADJ':
                    attributes.append(token.text)

        # Add type-specific attributes
        if 'programming' in entity_type.lower():
            if 'open source' in keyword or 'free' in keyword:
                attributes.append('open-source')
            if 'object oriented' in keyword or 'oop' in keyword:
                attributes.append('object-oriented')

        if 'framework' in entity_type.lower():
            attributes.extend(['framework', 'library', 'tool'])

        # Extract common descriptive terms
        descriptors = ['best', 'top', 'new', 'latest', 'advanced', 'beginner', 'professional']
        for desc in descriptors:
            if desc in keyword:
                attributes.append(desc)

        return list(set(attributes)) if attributes else ['general', 'standard']

    def _extract_relationships(self, keyword: str) -> List[Dict[str, str]]:
        """Extract relationships between entities"""
        relationships = []

        # Common relationship patterns
        relationship_patterns = {
            r'(\w+)\s+vs\s+(\w+)': 'compares_with',
            r'(\w+)\s+for\s+(\w+)': 'used_for',
            r'(\w+)\s+with\s+(\w+)': 'integrates_with',
            r'(\w+)\s+in\s+(\w+)': 'part_of',
        }

        for pattern, rel_type in relationship_patterns.items():
            matches = re.findall(pattern, keyword, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    relationships.append({
                        'entity': match[1],
                        'type': rel_type
                    })

        # Add implicit relationships based on entity type
        if 'python' in keyword:
            relationships.append({'entity': 'Programming', 'type': 'is_a'})
        if 'react' in keyword:
            relationships.append({'entity': 'JavaScript', 'type': 'depends_on'})
        if 'machine learning' in keyword:
            relationships.append({'entity': 'Data Science', 'type': 'part_of'})

        return relationships if relationships else [{'entity': 'General Knowledge', 'type': 'related_to'}]

    def _get_taxonomy(self, keyword: str) -> List[str]:
        """Get taxonomy classification"""
        # Check if we have a predefined taxonomy
        for key, taxonomy in self.TAXONOMY_MAPPINGS.items():
            if key in keyword:
                return taxonomy

        # Generate generic taxonomy
        return ['General', 'Concept', 'Information']

    def _get_ontology(self, keyword: str) -> Dict[str, Any]:
        """Get ontology hierarchy and parent concepts"""
        # Check if we have a predefined ontology
        for key, ontology in self.ONTOLOGY_HIERARCHIES.items():
            if key in keyword:
                return ontology

        # Generate generic ontology
        return {
            'hierarchy': ['Concept', 'General Concept', keyword.title()],
            'parent_concepts': ['Knowledge', 'Information']
        }

    def _extract_named_entities(self, keyword: str) -> List[str]:
        """Extract named entities using spaCy"""
        named_entities = []

        if self.nlp:
            doc = self.nlp(keyword)
            for ent in doc.ents:
                named_entities.append(ent.text)

        # If no entities found, extract capitalized words
        if not named_entities:
            words = keyword.split()
            named_entities = [word for word in words if word[0].isupper() and len(word) > 1]

        return named_entities if named_entities else [keyword]

    def _generate_disambiguations(self, keyword: str) -> List[str]:
        """Generate alternative meanings/disambiguations"""
        disambiguations = []

        # Common disambiguation patterns
        disambiguation_map = {
            'python': ['Python Programming Language', 'Python Snake', 'Monty Python'],
            'java': ['Java Programming Language', 'Java Island', 'Java Coffee'],
            'ruby': ['Ruby Programming Language', 'Ruby Gemstone', 'Ruby Color'],
            'react': ['React.js Library', 'Chemical Reaction', 'Response/Reaction'],
            'spring': ['Spring Framework', 'Spring Season', 'Spring Mechanism'],
            'angular': ['Angular Framework', 'Angular Measurement', 'Angular Shape'],
        }

        for key, disam in disambiguation_map.items():
            if key in keyword:
                return disam

        # Generate contextual disambiguations
        if len(keyword.split()) == 1:
            disambiguations = [
                f"{keyword} (Technology)",
                f"{keyword} (Concept)",
                f"{keyword} (General Term)"
            ]

        return disambiguations if disambiguations else [keyword]

    def _get_authority_sources(self, keyword: str, entity_type: str) -> List[str]:
        """Get authoritative sources for the entity"""
        sources = []

        # Type-specific authority sources
        if 'programming' in entity_type.lower() or 'technology' in entity_type.lower():
            sources = ['Stack Overflow', 'GitHub', 'Official Documentation', 'MDN Web Docs']
        elif 'marketing' in entity_type.lower():
            sources = ['Google', 'HubSpot', 'Moz', 'SEMrush']
        elif 'ai' in entity_type.lower() or 'machine learning' in entity_type.lower():
            sources = ['arXiv', 'Papers with Code', 'Google AI Blog', 'OpenAI']
        else:
            sources = ['Wikipedia', 'Academic Journals', 'Industry Publications']

        # Add keyword-specific sources
        if 'python' in keyword:
            sources.insert(0, 'Python.org')
        elif 'react' in keyword:
            sources.insert(0, 'React.dev')
        elif 'seo' in keyword:
            sources.insert(0, 'Google Search Central')

        return sources[:5]  # Limit to top 5

    def _calculate_confidence(self, keyword: str, entity_type: str) -> float:
        """Calculate confidence score for entity extraction"""
        confidence = 0.5  # Base confidence

        # Increase confidence if we found a specific entity type
        if entity_type != 'General Concept':
            confidence += 0.2

        # Increase confidence if spaCy model is available
        if self.nlp:
            confidence += 0.15

        # Increase confidence for well-known terms
        known_terms = ['python', 'java', 'react', 'seo', 'machine learning', 'ai']
        if any(term in keyword.lower() for term in known_terms):
            confidence += 0.15

        return min(round(confidence, 2), 1.0)
