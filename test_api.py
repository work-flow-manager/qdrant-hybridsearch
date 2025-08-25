#!/usr/bin/env python3
"""Test script for Qdrant Hybrid Search API"""

import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000"
API_KEY = "your-secure-api-key-here"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health check passed")
        print(f"   - Status: {data['status']}")
        print(f"   - GPU: {data['gpu_name'] if data['gpu_available'] else 'Not available'}")
        print(f"   - Qdrant: {'Connected' if data['qdrant_connected'] else 'Not connected'}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def test_index():
    """Test document indexing"""
    print("\n📝 Testing document indexing...")
    
    documents = {
        "documents": [
            {
                "text": "Python é uma linguagem de programação de alto nível, interpretada e de propósito geral.",
                "metadata": {"category": "programming", "language": "pt"}
            },
            {
                "text": "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
                "metadata": {"category": "ai", "language": "en"}
            },
            {
                "text": "Docker is a platform for developing, shipping, and running applications in containers.",
                "metadata": {"category": "devops", "language": "en"}
            }
        ]
    }
    
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(f"{API_URL}/index", json=documents, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Indexed {data['indexed_count']} documents")
        print(f"   - Processing time: {data['processing_time_ms']:.2f}ms")
        return True
    else:
        print(f"❌ Indexing failed: {response.status_code}")
        print(f"   - Error: {response.text}")
        return False

def test_search():
    """Test search functionality"""
    print("\n🔍 Testing search...")
    
    queries = [
        {"query": "programming languages", "mode": "hybrid"},
        {"query": "inteligência artificial", "mode": "dense"},
        {"query": "Docker containers", "mode": "sparse"}
    ]
    
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    for q in queries:
        print(f"\n   Query: '{q['query']}' (mode: {q['mode']})")
        response = requests.post(f"{API_URL}/search", json=q, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {len(data['results'])} results in {data['processing_time_ms']:.2f}ms")
            
            if data['results']:
                print("   Top result:")
                result = data['results'][0]
                print(f"     - Score: {result['score']:.4f}")
                print(f"     - Text: {result['text'][:100]}...")
        else:
            print(f"   ❌ Search failed: {response.status_code}")

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Qdrant Hybrid Search API Test Suite")
    print("=" * 60)
    
    # Wait for services to be ready
    print("\n⏳ Waiting for services to start...")
    time.sleep(5)
    
    # Run tests
    if test_health():
        time.sleep(2)
        if test_index():
            time.sleep(2)
            test_search()
    
    print("\n" + "=" * 60)
    print("✅ Tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()