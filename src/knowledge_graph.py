"""
Knowledge Graph Builder
Constructs knowledge graphs with nodes and edges representing entity relationships
"""

import logging
from typing import Dict, List, Any
import hashlib

logger = logging.getLogger(__name__)


class KnowledgeGraphBuilder:
    """
    Builds knowledge graphs representing entities and their relationships
    """

    def __init__(self):
        """Initialize knowledge graph builder"""
        logger.info("Initializing KnowledgeGraphBuilder")

    def build(self, keyword: str, entity_data: Dict[str, Any], semantic_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a knowledge graph for the keyword

        Args:
            keyword: The search keyword
            entity_data: Entity extraction data
            semantic_data: Semantic analysis data

        Returns:
            Knowledge graph with nodes and edges
        """
        logger.info(f"Building knowledge graph for: {keyword}")

        nodes = self._generate_nodes(keyword, entity_data, semantic_data)
        edges = self._generate_edges(keyword, entity_data, semantic_data, nodes)

        graph = {
            'nodes': nodes,
            'edges': edges,
            'metadata': {
                'node_count': len(nodes),
                'edge_count': len(edges),
                'graph_density': self._calculate_density(nodes, edges)
            }
        }

        logger.info(f"Knowledge graph built with {len(nodes)} nodes and {len(edges)} edges")
        return graph

    def _generate_nodes(self, keyword: str, entity_data: Dict[str, Any], semantic_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate nodes for the knowledge graph"""
        nodes = []

        # Main entity node
        main_node = {
            'id': self._generate_id(keyword),
            'label': entity_data.get('entity', keyword),
            'type': 'main_entity',
            'entity_type': entity_data.get('entity_type', 'Unknown'),
            'properties': {
                'name': entity_data.get('entity', keyword),
                'attributes': entity_data.get('attributes', []),
                'topic': semantic_data.get('topic', 'General')
            }
        }
        nodes.append(main_node)

        # Add related entity nodes from relationships
        for rel in entity_data.get('relationships', []):
            related_entity = rel.get('entity')
            if related_entity:
                node = {
                    'id': self._generate_id(related_entity),
                    'label': related_entity,
                    'type': 'related_entity',
                    'entity_type': rel.get('type', 'unknown'),
                    'properties': {
                        'name': related_entity,
                        'relationship_type': rel.get('type')
                    }
                }
                nodes.append(node)

        # Add topic cluster nodes
        for cluster_topic in semantic_data.get('topic_cluster', [])[:5]:
            node = {
                'id': self._generate_id(cluster_topic),
                'label': cluster_topic,
                'type': 'topic',
                'entity_type': 'Topic',
                'properties': {
                    'name': cluster_topic,
                    'domain': semantic_data.get('topic', 'General')
                }
            }
            nodes.append(node)

        # Add semantic relevance nodes (top 5)
        for rel_term in semantic_data.get('semantic_relevance', [])[:5]:
            node = {
                'id': self._generate_id(rel_term),
                'label': rel_term,
                'type': 'semantic_concept',
                'entity_type': 'Concept',
                'properties': {
                    'name': rel_term,
                    'relevance': 'high'
                }
            }
            nodes.append(node)

        # Add taxonomy nodes
        for tax_level in entity_data.get('taxonomy', [])[:3]:
            node = {
                'id': self._generate_id(tax_level),
                'label': tax_level,
                'type': 'taxonomy',
                'entity_type': 'Category',
                'properties': {
                    'name': tax_level,
                    'level': entity_data.get('taxonomy', []).index(tax_level)
                }
            }
            nodes.append(node)

        # Remove duplicates based on ID
        unique_nodes = {node['id']: node for node in nodes}
        return list(unique_nodes.values())

    def _generate_edges(self, keyword: str, entity_data: Dict[str, Any],
                       semantic_data: Dict[str, Any], nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate edges connecting nodes"""
        edges = []
        main_id = self._generate_id(keyword)
        node_ids = {node['id'] for node in nodes}

        # Create edges from main entity to related entities
        for rel in entity_data.get('relationships', []):
            related_entity = rel.get('entity')
            if related_entity:
                target_id = self._generate_id(related_entity)
                if target_id in node_ids:
                    edge = {
                        'id': self._generate_id(f"{main_id}_{target_id}"),
                        'source': main_id,
                        'target': target_id,
                        'type': rel.get('type', 'related_to'),
                        'properties': {
                            'relationship': rel.get('type', 'related_to'),
                            'weight': 1.0
                        }
                    }
                    edges.append(edge)

        # Create edges to topic clusters
        for cluster_topic in semantic_data.get('topic_cluster', [])[:5]:
            target_id = self._generate_id(cluster_topic)
            if target_id in node_ids:
                edge = {
                    'id': self._generate_id(f"{main_id}_{target_id}"),
                    'source': main_id,
                    'target': target_id,
                    'type': 'belongs_to_cluster',
                    'properties': {
                        'relationship': 'topic_cluster',
                        'weight': 0.8
                    }
                }
                edges.append(edge)

        # Create edges to semantic relevance terms
        for rel_term in semantic_data.get('semantic_relevance', [])[:5]:
            target_id = self._generate_id(rel_term)
            if target_id in node_ids:
                edge = {
                    'id': self._generate_id(f"{main_id}_{target_id}"),
                    'source': main_id,
                    'target': target_id,
                    'type': 'semantically_related',
                    'properties': {
                        'relationship': 'semantic_similarity',
                        'weight': 0.7
                    }
                }
                edges.append(edge)

        # Create hierarchical edges for taxonomy
        taxonomy = entity_data.get('taxonomy', [])
        for i in range(len(taxonomy) - 1):
            source_id = self._generate_id(taxonomy[i])
            target_id = self._generate_id(taxonomy[i + 1])
            if source_id in node_ids and target_id in node_ids:
                edge = {
                    'id': self._generate_id(f"{source_id}_{target_id}"),
                    'source': source_id,
                    'target': target_id,
                    'type': 'is_parent_of',
                    'properties': {
                        'relationship': 'taxonomy_hierarchy',
                        'weight': 0.9
                    }
                }
                edges.append(edge)

        # Connect main entity to its taxonomy
        if taxonomy:
            target_id = self._generate_id(taxonomy[-1])
            if target_id in node_ids:
                edge = {
                    'id': self._generate_id(f"{main_id}_{target_id}"),
                    'source': main_id,
                    'target': target_id,
                    'type': 'categorized_as',
                    'properties': {
                        'relationship': 'taxonomy_classification',
                        'weight': 0.95
                    }
                }
                edges.append(edge)

        return edges

    def _generate_id(self, text: str) -> str:
        """Generate a unique ID for a node or edge"""
        # Use MD5 hash of lowercase text for consistent IDs
        return hashlib.md5(text.lower().encode()).hexdigest()[:16]

    def _calculate_density(self, nodes: List[Dict], edges: List[Dict]) -> float:
        """Calculate graph density (ratio of actual edges to possible edges)"""
        n = len(nodes)
        if n <= 1:
            return 0.0

        max_edges = n * (n - 1)  # For directed graph
        actual_edges = len(edges)

        density = actual_edges / max_edges if max_edges > 0 else 0.0
        return round(density, 4)

    def export_to_cypher(self, graph: Dict[str, Any]) -> List[str]:
        """
        Export knowledge graph to Cypher queries for Neo4j

        Args:
            graph: Knowledge graph dictionary

        Returns:
            List of Cypher CREATE statements
        """
        cypher_queries = []

        # Create node queries
        for node in graph['nodes']:
            props = ', '.join([f"{k}: '{v}'" if isinstance(v, str) else f"{k}: {v}"
                              for k, v in node['properties'].items()])
            query = f"CREATE (n:{node['type']} {{id: '{node['id']}', label: '{node['label']}', {props}}})"
            cypher_queries.append(query)

        # Create edge queries
        for edge in graph['edges']:
            query = f"MATCH (a {{id: '{edge['source']}'}}), (b {{id: '{edge['target']}'}}) CREATE (a)-[r:{edge['type']}]->(b)"
            cypher_queries.append(query)

        return cypher_queries

    def export_to_rdf(self, graph: Dict[str, Any]) -> str:
        """
        Export knowledge graph to RDF/Turtle format

        Args:
            graph: Knowledge graph dictionary

        Returns:
            RDF Turtle string
        """
        rdf_lines = ["@prefix kg: <http://example.org/kg#> .", ""]

        # Add nodes as RDF subjects
        for node in graph['nodes']:
            rdf_lines.append(f"kg:{node['id']} a kg:{node['type']} ;")
            rdf_lines.append(f"  kg:label \"{node['label']}\" ;")
            for key, value in node['properties'].items():
                rdf_lines.append(f"  kg:{key} \"{value}\" ;")
            rdf_lines[-1] = rdf_lines[-1].rstrip(';') + ' .'
            rdf_lines.append("")

        # Add edges as RDF predicates
        for edge in graph['edges']:
            rdf_lines.append(f"kg:{edge['source']} kg:{edge['type']} kg:{edge['target']} .")

        return "\n".join(rdf_lines)
