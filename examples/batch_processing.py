"""
Batch Processing Example
Demonstrates analyzing multiple keywords in parallel
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyzer import KeywordAnalyzer
import json
import time


def main():
    """Batch processing example"""
    print("=" * 60)
    print("Semantic Keyword Analysis Tool - Batch Processing")
    print("=" * 60)

    # Initialize analyzer
    print("\n1. Initializing analyzer with 4 workers...")
    analyzer = KeywordAnalyzer(use_cache=True, max_workers=4)

    # Define keywords to analyze
    keywords = [
        "python programming",
        "react framework",
        "machine learning",
        "docker containers",
        "seo optimization",
        "fastapi python",
        "kubernetes deployment",
        "neural networks",
        "web development",
        "cloud computing"
    ]

    print(f"\n2. Analyzing {len(keywords)} keywords in parallel...")
    print("Keywords to analyze:")
    for i, kw in enumerate(keywords, 1):
        print(f"  {i}. {kw}")

    # Measure performance
    start_time = time.time()

    # Batch analysis
    results = analyzer.analyze_batch(keywords, parallel=True)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Display results summary
    print("\n3. Analysis Results Summary:")
    print("-" * 60)

    successful = 0
    errors = 0

    for keyword, result in results.items():
        if hasattr(result, 'entity'):
            successful += 1
            print(f"\n✓ {keyword}")
            print(f"  Entity Type: {result.entity_type}")
            print(f"  Topic: {result.topic}")
            print(f"  Salience: {result.salience}/100")
            print(f"  Authority: {result.topical_authority}/100")
            print(f"  Search Intent: {result.search_intent}")
        else:
            errors += 1
            print(f"\n✗ {keyword}")
            print(f"  Error: {result.get('error', 'Unknown error')}")

    # Performance metrics
    print("\n" + "=" * 60)
    print("Performance Metrics:")
    print("-" * 60)
    print(f"Total Keywords: {len(keywords)}")
    print(f"Successful: {successful}")
    print(f"Errors: {errors}")
    print(f"Total Time: {elapsed_time:.2f} seconds")
    print(f"Average Time per Keyword: {elapsed_time/len(keywords):.2f} seconds")
    print(f"Keywords per Second: {len(keywords)/elapsed_time:.2f}")

    # Create a comparison table
    print("\n" + "=" * 60)
    print("Keyword Comparison Table:")
    print("-" * 60)
    print(f"{'Keyword':<25} {'Type':<25} {'Salience':<12} {'Authority':<12}")
    print("-" * 60)

    for keyword, result in results.items():
        if hasattr(result, 'entity'):
            print(f"{keyword:<25} {result.entity_type:<25} {result.salience:<12.1f} {result.topical_authority:<12.1f}")

    # Find highest scoring keywords
    print("\n" + "=" * 60)
    print("Top Keywords by Score:")
    print("-" * 60)

    # Sort by salience
    sorted_by_salience = sorted(
        [(kw, res) for kw, res in results.items() if hasattr(res, 'salience')],
        key=lambda x: x[1].salience,
        reverse=True
    )

    print("\nTop 3 by Salience:")
    for i, (kw, res) in enumerate(sorted_by_salience[:3], 1):
        print(f"  {i}. {kw}: {res.salience}/100")

    # Sort by authority
    sorted_by_authority = sorted(
        [(kw, res) for kw, res in results.items() if hasattr(res, 'topical_authority')],
        key=lambda x: x[1].topical_authority,
        reverse=True
    )

    print("\nTop 3 by Authority:")
    for i, (kw, res) in enumerate(sorted_by_authority[:3], 1):
        print(f"  {i}. {kw}: {res.topical_authority}/100")

    # Save all results to JSON
    output_file = "batch_analysis_results.json"
    print(f"\n4. Saving results to {output_file}...")

    serializable_results = {}
    for keyword, result in results.items():
        if hasattr(result, 'to_dict'):
            serializable_results[keyword] = result.to_dict()
        else:
            serializable_results[keyword] = result

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)

    print(f"✓ Results saved successfully")

    # Cache statistics
    print("\n" + "=" * 60)
    print("Cache Statistics:")
    cache_stats = analyzer.get_cache_stats()
    print(f"Cached Keywords: {cache_stats['cached_keywords']}")

    print("\n" + "=" * 60)
    print("Batch Processing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
