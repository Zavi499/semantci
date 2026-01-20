"""
Async Processing Example
Demonstrates asynchronous keyword analysis
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from src.analyzer import KeywordAnalyzer
import time


async def analyze_single_async(analyzer, keyword):
    """Analyze a single keyword asynchronously"""
    print(f"  Analyzing: {keyword}")
    result = await analyzer.analyze_async(keyword)
    print(f"  ✓ Completed: {keyword} -> {result.entity_type}")
    return result


async def main():
    """Async processing example"""
    print("=" * 60)
    print("Semantic Keyword Analysis Tool - Async Processing")
    print("=" * 60)

    # Initialize analyzer
    print("\n1. Initializing analyzer...")
    analyzer = KeywordAnalyzer(use_cache=True)

    # Example 1: Single async analysis
    print("\n2. Single async analysis...")
    keyword = "python programming"

    start = time.time()
    result = await analyzer.analyze_async(keyword)
    elapsed = time.time() - start

    print(f"✓ Analysis completed in {elapsed:.2f}s")
    print(f"  Entity: {result.entity}")
    print(f"  Type: {result.entity_type}")
    print(f"  Topic: {result.topic}")

    # Example 2: Concurrent async analyses
    print("\n3. Concurrent async analyses...")
    keywords = [
        "react framework",
        "machine learning",
        "docker containers",
        "fastapi python",
        "kubernetes"
    ]

    print(f"Analyzing {len(keywords)} keywords concurrently...")

    start = time.time()

    # Create tasks for concurrent execution
    tasks = [analyze_single_async(analyzer, kw) for kw in keywords]

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start

    print(f"\n✓ All analyses completed in {elapsed:.2f}s")
    print(f"  Average time per keyword: {elapsed/len(keywords):.2f}s")

    # Display results summary
    print("\n4. Results Summary:")
    print("-" * 60)
    for keyword, result in zip(keywords, results):
        print(f"{keyword:<25} -> {result.entity_type:<25} (Salience: {result.salience})")

    # Example 3: Async batch analysis
    print("\n5. Async batch analysis...")
    batch_keywords = [
        "artificial intelligence",
        "neural networks",
        "cloud computing",
        "devops",
        "microservices",
        "blockchain",
        "cybersecurity"
    ]

    print(f"Batch analyzing {len(batch_keywords)} keywords...")

    start = time.time()
    batch_results = await analyzer.analyze_batch_async(batch_keywords)
    elapsed = time.time() - start

    print(f"✓ Batch completed in {elapsed:.2f}s")

    successful = sum(1 for r in batch_results.values() if hasattr(r, 'entity'))
    errors = len(batch_results) - successful

    print(f"  Successful: {successful}")
    print(f"  Errors: {errors}")

    # Display batch results
    print("\n6. Batch Results:")
    print("-" * 60)
    for keyword, result in batch_results.items():
        if hasattr(result, 'entity'):
            print(f"✓ {keyword}")
            print(f"  Type: {result.entity_type}")
            print(f"  Topic: {result.topic}")
            print(f"  Authority: {result.topical_authority}/100")
        else:
            print(f"✗ {keyword}: {result.get('error', 'Unknown error')}")

    # Example 4: Mixed async operations
    print("\n7. Mixed async operations...")

    async def process_keyword(kw):
        """Process keyword and extract specific info"""
        result = await analyzer.analyze_async(kw)
        return {
            'keyword': kw,
            'entity': result.entity,
            'topic': result.topic,
            'salience': result.salience,
            'intent': result.search_intent
        }

    keywords_to_process = ["python", "javascript", "go", "rust"]

    start = time.time()
    tasks = [process_keyword(kw) for kw in keywords_to_process]
    processed_results = await asyncio.gather(*tasks)
    elapsed = time.time() - start

    print(f"✓ Processed {len(processed_results)} keywords in {elapsed:.2f}s")

    for item in processed_results:
        print(f"\n  {item['keyword']}:")
        print(f"    Entity: {item['entity']}")
        print(f"    Topic: {item['topic']}")
        print(f"    Salience: {item['salience']}/100")
        print(f"    Intent: {item['intent']}")

    # Performance comparison
    print("\n" + "=" * 60)
    print("Performance Summary:")
    print("-" * 60)
    print("Async processing allows concurrent operations,")
    print("significantly improving throughput for I/O-bound tasks.")

    print("\n" + "=" * 60)
    print("Async Processing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
