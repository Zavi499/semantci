"""
API Client Example
Demonstrates using the FastAPI endpoints
"""

import requests
import json
import time


class KeywordAnalysisClient:
    """Client for the Keyword Analysis API"""

    def __init__(self, base_url="http://localhost:8000"):
        """Initialize the client"""
        self.base_url = base_url

    def health_check(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

    def analyze(self, keyword):
        """Analyze a single keyword"""
        response = requests.post(
            f"{self.base_url}/analyze",
            json={"keyword": keyword}
        )
        return response.json()

    def analyze_get(self, keyword):
        """Analyze a single keyword using GET"""
        response = requests.get(f"{self.base_url}/analyze/{keyword}")
        return response.json()

    def analyze_batch(self, keywords, parallel=True):
        """Analyze multiple keywords"""
        response = requests.post(
            f"{self.base_url}/analyze/batch",
            json={"keywords": keywords, "parallel": parallel}
        )
        return response.json()

    def clear_cache(self):
        """Clear the analysis cache"""
        response = requests.delete(f"{self.base_url}/cache")
        return response.json()

    def get_cache_stats(self):
        """Get cache statistics"""
        response = requests.get(f"{self.base_url}/cache/stats")
        return response.json()


def main():
    """API client example"""
    print("=" * 60)
    print("Keyword Analysis API Client Example")
    print("=" * 60)

    # Initialize client
    client = KeywordAnalysisClient()

    # 1. Health check
    print("\n1. Checking API health...")
    try:
        health = client.health_check()
        print(f"✓ API Status: {health['status']}")
        print(f"  Version: {health['version']}")
        print(f"  Cache Stats: {health['cache_stats']}")
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to API")
        print("  Make sure the API server is running:")
        print("  python -m uvicorn api.main:app --reload")
        return

    # 2. Single keyword analysis (POST)
    print("\n2. Analyzing single keyword (POST)...")
    keyword = "python programming"
    print(f"Keyword: '{keyword}'")

    start = time.time()
    result = client.analyze(keyword)
    elapsed = time.time() - start

    if result['success']:
        data = result['data']
        print(f"✓ Analysis completed in {elapsed:.2f}s")
        print(f"  Entity: {data['entity']}")
        print(f"  Type: {data['entity_type']}")
        print(f"  Topic: {data['topic']}")
        print(f"  Salience: {data['salience']}/100")
        print(f"  Authority: {data['topical_authority']}/100")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")

    # 3. Single keyword analysis (GET)
    print("\n3. Analyzing single keyword (GET)...")
    keyword2 = "react"
    print(f"Keyword: '{keyword2}'")

    start = time.time()
    result2 = client.analyze_get(keyword2)
    elapsed = time.time() - start

    if result2['success']:
        data = result2['data']
        print(f"✓ Analysis completed in {elapsed:.2f}s")
        print(f"  Entity: {data['entity']}")
        print(f"  Type: {data['entity_type']}")
        print(f"  Search Intent: {data['search_intent']}")

    # 4. Batch analysis
    print("\n4. Analyzing batch of keywords...")
    keywords = [
        "machine learning",
        "docker",
        "seo",
        "fastapi",
        "kubernetes"
    ]

    print(f"Keywords: {', '.join(keywords)}")

    start = time.time()
    batch_result = client.analyze_batch(keywords, parallel=True)
    elapsed = time.time() - start

    print(f"✓ Batch analysis completed in {elapsed:.2f}s")
    print(f"  Processed: {batch_result['processed']} keywords")
    print(f"  Average time: {elapsed/len(keywords):.2f}s per keyword")

    if batch_result['errors']:
        print(f"  Errors: {len(batch_result['errors'])}")

    # Display batch results
    print("\n  Results:")
    for keyword, result in batch_result['results'].items():
        if 'error' not in result:
            print(f"    ✓ {keyword}: {result['entity_type']} (Salience: {result['salience']})")
        else:
            print(f"    ✗ {keyword}: {result['error']}")

    # 5. Cache statistics
    print("\n5. Cache Statistics...")
    cache_stats = client.get_cache_stats()
    print(f"Cached Keywords: {cache_stats['cached_keywords']}")
    print(f"Cache Enabled: {cache_stats['cache_enabled']}")

    # 6. Test cache performance
    print("\n6. Testing cache performance...")
    print(f"Re-analyzing '{keyword}' (should be cached)...")

    start = time.time()
    cached_result = client.analyze(keyword)
    elapsed = time.time() - start

    print(f"✓ Analysis completed in {elapsed:.2f}s (from cache)")
    print(f"  Speedup: {(result['data'] == cached_result['data'])}")

    # 7. Save results to file
    print("\n7. Saving batch results to file...")
    output_file = "api_batch_results.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(batch_result, f, indent=2, ensure_ascii=False)

    print(f"✓ Results saved to: {output_file}")

    # 8. Clear cache
    print("\n8. Clearing cache...")
    clear_result = client.clear_cache()
    print(f"✓ {clear_result['message']}")

    # Verify cache cleared
    cache_stats = client.get_cache_stats()
    print(f"Cached Keywords: {cache_stats['cached_keywords']}")

    print("\n" + "=" * 60)
    print("API Client Example Complete!")
    print("=" * 60)
    print("\nTip: Visit http://localhost:8000/docs for interactive API documentation")


if __name__ == "__main__":
    main()
