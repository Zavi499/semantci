"""
Schema.org Markup Builder
Generates structured data markup for entities
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class SchemaBuilder:
    """
    Generates Schema.org structured data markup for entities
    """

    # Schema type mappings
    SCHEMA_TYPE_MAPPINGS = {
        'Programming Language': 'SoftwareApplication',
        'Framework': 'SoftwareApplication',
        'Technology': 'Product',
        'Cloud Platform': 'Product',
        'Database': 'SoftwareApplication',
        'DevOps': 'Product',
        'Digital Marketing': 'Service',
        'Artificial Intelligence': 'TechArticle',
        'Educational Content': 'Article',
        'Commercial': 'Product',
        'Service': 'Service',
        'General Concept': 'Thing'
    }

    def __init__(self):
        """Initialize schema builder"""
        logger.info("Initializing SchemaBuilder")

    def generate(self, keyword: str, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Schema.org structured data

        Args:
            keyword: The search keyword
            entity_data: Entity extraction data

        Returns:
            Schema.org JSON-LD markup
        """
        logger.info(f"Generating schema for: {keyword}")

        entity_type = entity_data.get('entity_type', 'General Concept')
        schema_type = self._get_schema_type(entity_type)

        schema = {
            '@context': 'https://schema.org',
            '@type': schema_type,
            'name': entity_data.get('entity', keyword),
            'description': self._generate_description(keyword, entity_data),
            'additionalType': entity_type,
            'identifier': keyword.replace(' ', '-').lower()
        }

        # Add type-specific properties
        schema['properties'] = self._add_type_specific_properties(
            schema_type, keyword, entity_data
        )

        # Add relationships as related items
        if entity_data.get('relationships'):
            schema['relatedLink'] = self._format_relationships(entity_data['relationships'])

        # Add attributes
        if entity_data.get('attributes'):
            schema['keywords'] = ', '.join(entity_data['attributes'])

        # Add authority sources as references
        if entity_data.get('authority_sources'):
            schema['about'] = [
                {'@type': 'Thing', 'name': source}
                for source in entity_data['authority_sources'][:3]
            ]

        logger.info(f"Schema generated for: {keyword}")
        return schema

    def _get_schema_type(self, entity_type: str) -> str:
        """Map entity type to Schema.org type"""
        return self.SCHEMA_TYPE_MAPPINGS.get(entity_type, 'Thing')

    def _generate_description(self, keyword: str, entity_data: Dict[str, Any]) -> str:
        """Generate a description for the schema"""
        entity = entity_data.get('entity', keyword)
        entity_type = entity_data.get('entity_type', 'concept')
        attributes = entity_data.get('attributes', [])

        description = f"{entity} is a {entity_type.lower()}"

        if attributes:
            attr_text = ', '.join(attributes[:3])
            description += f" characterized by {attr_text}"

        return description

    def _add_type_specific_properties(self, schema_type: str, keyword: str,
                                     entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add properties specific to the schema type"""
        properties = {}

        if schema_type == 'SoftwareApplication':
            properties.update({
                'applicationCategory': entity_data.get('entity_type', 'Technology'),
                'operatingSystem': 'Multi-platform',
                'softwareVersion': 'Latest'
            })

        elif schema_type == 'Product':
            properties.update({
                'category': entity_data.get('entity_type', 'Technology'),
                'brand': {'@type': 'Brand', 'name': entity_data.get('entity', keyword)}
            })

        elif schema_type == 'Service':
            properties.update({
                'serviceType': entity_data.get('entity_type', 'Service'),
                'provider': {'@type': 'Organization', 'name': 'Industry Standard'}
            })

        elif schema_type == 'Article' or schema_type == 'TechArticle':
            properties.update({
                'articleSection': entity_data.get('entity_type', 'Technology'),
                'author': {'@type': 'Organization', 'name': 'Community'},
                'datePublished': datetime.now().isoformat()
            })

        # Add common properties
        properties['url'] = f"https://example.com/{keyword.replace(' ', '-').lower()}"

        return properties

    def _format_relationships(self, relationships: List[Dict[str, str]]) -> List[str]:
        """Format relationships as related links"""
        links = []
        for rel in relationships[:5]:  # Limit to 5
            entity = rel.get('entity', '')
            if entity:
                links.append(f"https://example.com/{entity.replace(' ', '-').lower()}")
        return links

    def generate_breadcrumb(self, taxonomy: List[str]) -> Dict[str, Any]:
        """
        Generate BreadcrumbList schema from taxonomy

        Args:
            taxonomy: List of taxonomy levels

        Returns:
            BreadcrumbList schema
        """
        breadcrumb = {
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': []
        }

        for position, item in enumerate(taxonomy, start=1):
            breadcrumb['itemListElement'].append({
                '@type': 'ListItem',
                'position': position,
                'name': item,
                'item': f"https://example.com/{item.replace(' ', '-').lower()}"
            })

        return breadcrumb

    def generate_faq(self, keyword: str, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate FAQ schema for the keyword

        Args:
            keyword: The search keyword
            entity_data: Entity extraction data

        Returns:
            FAQPage schema
        """
        entity = entity_data.get('entity', keyword)
        entity_type = entity_data.get('entity_type', 'concept')

        faq = {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': [
                {
                    '@type': 'Question',
                    'name': f"What is {entity}?",
                    'acceptedAnswer': {
                        '@type': 'Answer',
                        'text': f"{entity} is a {entity_type.lower()} used in various applications."
                    }
                },
                {
                    '@type': 'Question',
                    'name': f"What are the key features of {entity}?",
                    'acceptedAnswer': {
                        '@type': 'Answer',
                        'text': f"Key features include: {', '.join(entity_data.get('attributes', ['various capabilities']))}"
                    }
                }
            ]
        }

        return faq
