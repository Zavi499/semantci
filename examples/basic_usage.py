"""
Basic Usage Example
Demonstrates simple keyword analysis
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyzer import KeywordAnalyzer
import json


def main():
    """Basic usage example"""
    print("=" * 60)
    print("Semantic Keyword Analysis Tool - Basic Usage")
    print("=" * 60)

    # Initialize analyzer
    print("\n1. Initializing analyzer...")
    analyzer = KeywordAnalyzer(use_cache=True)

    # Analyze a single keyword
    keyword = "python programming"
    print(f"\n2. Analyzing keyword: '{keyword}'")

    result = analyzer.analyze(keyword)

    # Display results
    print("\n3. Analysis Results:")
    print("-" * 60)
    print(f"Entity: {result.entity}")
    print(f"Entity Type: {result.entity_type}")
    print(f"Topic: {result.topic}")
    print(f"Search Intent: {result.search_intent}")
    print(f"\nAttributes: {', '.join(result.attributes)}")
    print(f"\nSemantic Relevance (top 5):")
    for term in result.semantic_relevance[:5]:
        print(f"  - {term}")

    print(f"\nTopic Cluster:")
    for topic in result.topic_cluster[:5]:
        print(f"  - {topic}")

    print(f"\nRelationships:")
    for rel in result.relationships[:3]:
        print(f"  - {rel['entity']} ({rel['type']})")

    print(f"\nScores:")
    print(f"  - Salience: {result.salience}/100")
    print(f"  - Topical Authority: {result.topical_authority}/100")
    print(f"  - Overall Confidence: {result.confidence_scores['overall']}")

    print(f"\nKnowledge Graph:")
    print(f"  - Nodes: {result.knowledge_graph['metadata']['node_count']}")
    print(f"  - Edges: {result.knowledge_graph['metadata']['edge_count']}")

    # Save full results to JSON
    output_file = "keyword_analysis_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

    print(f"\n4. Full results saved to: {output_file}")

    # Analyze another keyword
    print("\n" + "=" * 60)
    keyword2 = "machine learning"
    print(f"Analyzing another keyword: '{keyword2}'")

    result2 = analyzer.analyze(keyword2)

    print(f"\nEntity: {result2.entity}")
    print(f"Entity Type: {result2.entity_type}")
    print(f"Topic: {result2.topic}")
    print(f"Salience: {result2.salience}/100")
    print(f"Authority: {result2.topical_authority}/100")

    # Show cache statistics
    print("\n" + "=" * 60)
    print("Cache Statistics:")
    cache_stats = analyzer.get_cache_stats()
    print(f"Cached Keywords: {cache_stats['cached_keywords']}")
    print(f"Cache Enabled: {cache_stats['cache_enabled']}")

    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
