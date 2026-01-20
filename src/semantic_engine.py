"""
Semantic Analysis Engine
Analyzes semantic meaning, intent, relevance, and topic clustering
"""

import logging
from typing import Dict, List, Any
import re
from collections import Counter
import spacy

logger = logging.getLogger(__name__)


class SemanticEngine:
    """
    Performs semantic analysis on keywords including intent detection,
    topic clustering, and semantic relevance identification
    """

    # Search intent patterns
    INTENT_PATTERNS = {
        'informational': [
            r'\b(what|how|why|when|where|who|guide|tutorial|learn|understand)\b',
            r'\b(information|about|explain|definition|meaning)\b'
        ],
        'navigational': [
            r'\b(login|sign in|website|official|homepage|portal)\b',
            r'\b(site|page|download|app)\b'
        ],
        'transactional': [
            r'\b(buy|purchase|order|shop|price|cost|deal|discount)\b',
            r'\b(hire|book|register|subscribe|get|find)\b'
        ],
        'commercial': [
            r'\b(best|top|review|compare|vs|versus|alternative)\b',
            r'\b(cheap|affordable|premium|professional)\b'
        ]
    }

    # Topic classifications
    TOPIC_DOMAINS = {
        'Technology': [
            'programming', 'software', 'hardware', 'computer', 'code', 'development',
            'web', 'app', 'api', 'database', 'cloud', 'ai', 'machine learning'
        ],
        'Business': [
            'marketing', 'seo', 'sales', 'entrepreneur', 'startup', 'finance',
            'management', 'strategy', 'analytics', 'commerce'
        ],
        'Education': [
            'learn', 'course', 'tutorial', 'training', 'study', 'education',
            'school', 'university', 'certification', 'teaching'
        ],
        'Health': [
            'health', 'fitness', 'medical', 'doctor', 'nutrition', 'exercise',
            'wellness', 'disease', 'treatment', 'medicine'
        ],
        'Entertainment': [
            'game', 'movie', 'music', 'video', 'stream', 'entertainment',
            'sport', 'media', 'content', 'show'
        ]
    }

    # Semantic relevance mappings
    SEMANTIC_MAPPINGS = {
        'python': ['programming', 'coding', 'scripting', 'software development', 'automation',
                   'data science', 'web development', 'django', 'flask', 'pandas'],
        'react': ['javascript', 'frontend', 'ui', 'web development', 'component',
                  'jsx', 'hooks', 'redux', 'next.js', 'typescript'],
        'seo': ['search engine optimization', 'ranking', 'keywords', 'backlinks',
                'organic traffic', 'serp', 'google', 'content marketing', 'meta tags'],
        'machine learning': ['ai', 'neural networks', 'deep learning', 'algorithms',
                             'data science', 'predictive analytics', 'supervised learning',
                             'unsupervised learning', 'tensorflow', 'pytorch'],
        'docker': ['containers', 'containerization', 'devops', 'kubernetes',
                   'microservices', 'deployment', 'virtualization', 'images'],
    }

    # Topic clusters
    TOPIC_CLUSTERS = {
        'python': ['Python Programming', 'Web Development', 'Data Science', 'Automation', 'Backend Development'],
        'react': ['Frontend Development', 'JavaScript Ecosystem', 'UI/UX', 'Single Page Applications', 'Component Architecture'],
        'seo': ['Digital Marketing', 'Content Strategy', 'Search Marketing', 'Web Analytics', 'Online Visibility'],
        'machine learning': ['Artificial Intelligence', 'Data Science', 'Predictive Modeling', 'Neural Networks', 'Deep Learning'],
        'docker': ['DevOps', 'Cloud Computing', 'Containerization', 'Microservices', 'Infrastructure'],
    }

    def __init__(self):
        """Initialize semantic engine"""
        logger.info("Initializing SemanticEngine")
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found, using fallback mode")
            self.nlp = None
        logger.info("SemanticEngine initialized")

    def analyze(self, keyword: str) -> Dict[str, Any]:
        """
        Perform comprehensive semantic analysis

        Args:
            keyword: Input keyword to analyze

        Returns:
            Dictionary containing semantic analysis data
        """
        logger.info(f"Performing semantic analysis on: {keyword}")

        keyword_lower = keyword.lower().strip()

        # Detect search intent
        search_intent = self._detect_search_intent(keyword_lower)

        # Generate context
        context = self._generate_context(keyword_lower)

        # Extract semantic relevance
        semantic_relevance = self._extract_semantic_relevance(keyword_lower)

        # Identify topic
        topic = self._identify_topic(keyword_lower)

        # Generate topic cluster
        topic_cluster = self._generate_topic_cluster(keyword_lower)

        # Calculate confidence
        confidence = self._calculate_confidence(keyword_lower, search_intent, topic)

        result = {
            'search_intent': search_intent,
            'context': context,
            'semantic_relevance': semantic_relevance,
            'topic': topic,
            'topic_cluster': topic_cluster,
            'confidence': confidence
        }

        logger.info(f"Semantic analysis completed for: {keyword}")
        return result

    def _detect_search_intent(self, keyword: str) -> str:
        """Detect the primary search intent"""
        intent_scores = {intent: 0 for intent in self.INTENT_PATTERNS.keys()}

        # Score each intent type
        for intent_type, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, keyword, re.IGNORECASE):
                    intent_scores[intent_type] += 1

        # Find highest scoring intent
        max_score = max(intent_scores.values())
        if max_score > 0:
            for intent, score in intent_scores.items():
                if score == max_score:
                    return intent

        # Default to informational
        return 'informational'

    def _generate_context(self, keyword: str) -> str:
        """Generate contextual description of keyword usage"""
        contexts = {
            'informational': f"Users searching for '{keyword}' are seeking information, knowledge, or understanding about the topic.",
            'navigational': f"Users are trying to find a specific website, page, or resource related to '{keyword}'.",
            'transactional': f"Users intend to complete a transaction, purchase, or action related to '{keyword}'.",
            'commercial': f"Users are in the research phase, comparing options or looking for the best '{keyword}' solutions."
        }

        intent = self._detect_search_intent(keyword)
        base_context = contexts.get(intent, f"Users are searching for content related to '{keyword}'.")

        # Add topic-specific context
        topic = self._identify_topic(keyword)
        if topic != 'General':
            base_context += f" This query falls within the {topic} domain."

        # Add specific keyword context
        if 'tutorial' in keyword or 'how to' in keyword:
            base_context += " They are looking for step-by-step guidance or educational content."
        elif 'best' in keyword or 'top' in keyword:
            base_context += " They want recommendations and comparative analysis."
        elif 'vs' in keyword or 'versus' in keyword:
            base_context += " They are comparing different options to make an informed decision."

        return base_context

    def _extract_semantic_relevance(self, keyword: str) -> List[str]:
        """Extract semantically relevant terms"""
        relevant_terms = set()

        # Check predefined mappings
        for key, terms in self.SEMANTIC_MAPPINGS.items():
            if key in keyword:
                relevant_terms.update(terms[:10])  # Limit to top 10

        # Extract from the keyword itself
        words = keyword.split()
        for word in words:
            if len(word) > 3:  # Only meaningful words
                relevant_terms.add(word)

        # Add topic-related terms
        topic = self._identify_topic(keyword)
        if topic in self.TOPIC_DOMAINS:
            relevant_terms.update(self.TOPIC_DOMAINS[topic][:5])

        # Use spaCy for similarity if available
        if self.nlp and len(relevant_terms) < 5:
            doc = self.nlp(keyword)
            for token in doc:
                if token.pos_ in ['NOUN', 'VERB', 'ADJ'] and not token.is_stop:
                    relevant_terms.add(token.lemma_)

        # If still empty, add generic terms
        if not relevant_terms:
            relevant_terms = {keyword, 'related', 'similar', 'associated'}

        return sorted(list(relevant_terms))[:15]  # Return top 15

    def _identify_topic(self, keyword: str) -> str:
        """Identify the primary topic/subject area"""
        topic_scores = Counter()

        # Score each topic domain
        for topic, keywords_list in self.TOPIC_DOMAINS.items():
            for kw in keywords_list:
                if kw in keyword:
                    topic_scores[topic] += 1

        # Return highest scoring topic
        if topic_scores:
            return topic_scores.most_common(1)[0][0]

        # Default topic
        return 'General'

    def _generate_topic_cluster(self, keyword: str) -> List[str]:
        """Generate related topic clusters"""
        # Check predefined clusters
        for key, cluster in self.TOPIC_CLUSTERS.items():
            if key in keyword:
                return cluster

        # Generate based on topic
        topic = self._identify_topic(keyword)
        if topic in self.TOPIC_DOMAINS:
            related_topics = [f"{topic} Fundamentals", f"{topic} Best Practices",
                            f"{topic} Trends", f"{topic} Tools", f"{topic} Resources"]
            return related_topics

        # Generate generic clusters
        return [
            f"{keyword.title()} Overview",
            f"{keyword.title()} Applications",
            f"{keyword.title()} Resources",
            "Related Concepts",
            "Industry Trends"
        ]

    def _calculate_confidence(self, keyword: str, intent: str, topic: str) -> float:
        """Calculate confidence score for semantic analysis"""
        confidence = 0.5  # Base confidence

        # Increase if we detected a clear intent
        if intent != 'informational' or any(pattern in keyword for patterns in self.INTENT_PATTERNS.values() for pattern in patterns):
            confidence += 0.15

        # Increase if we identified a specific topic
        if topic != 'General':
            confidence += 0.15

        # Increase if we have semantic mappings
        if any(key in keyword for key in self.SEMANTIC_MAPPINGS.keys()):
            confidence += 0.15

        # Increase if spaCy is available
        if self.nlp:
            confidence += 0.05

        return min(round(confidence, 2), 1.0)

    def get_word_embeddings(self, keyword: str) -> List[str]:
        """Get semantically similar words using word embeddings"""
        if not self.nlp:
            return []

        similar_words = []
        try:
            doc = self.nlp(keyword)
            for token in doc:
                if token.has_vector:
                    # Get most similar tokens (this is simplified)
                    similar_words.append(token.text)
        except Exception as e:
            logger.warning(f"Error getting word embeddings: {e}")

        return similar_words[:10]
