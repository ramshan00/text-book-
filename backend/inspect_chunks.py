"""
Script to inspect actual chunk content in Qdrant and identify malformed data
"""

import os
import sys
import json
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

from retrieving import RAGRetriever

def inspect_chunks():
    """Inspect actual chunks being retrieved"""
    print("="*70)
    print("INSPECTING QDRANT CHUNKS")
    print("="*70)
    
    retriever = RAGRetriever()
    
    # Test with the same query from production
    query = "hello"
    print(f"\nQuery: '{query}'")
    
    json_response = retriever.retrieve(query_text=query, top_k=5, threshold=0.0)
    results = json.loads(json_response)
    
    chunks = results.get('results', [])
    print(f"\nRetrieved {len(chunks)} chunks\n")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\n{'='*70}")
        print(f"CHUNK {i}")
        print(f"{'='*70}")
        
        content = chunk.get('content', '')
        url = chunk.get('url', '')
        score = chunk.get('similarity_score', 0)
        
        print(f"URL: {url}")
        print(f"Score: {score:.3f}")
        print(f"Content type: {type(content).__name__}")
        print(f"Content length: {len(str(content))}")
        
        # Show raw content
        print(f"\nRAW CONTENT (first 500 chars):")
        print("-"*70)
        print(repr(content[:500]))
        print("-"*70)
        
        # Check for issues
        if not isinstance(content, str):
            print(f"\n❌ PROBLEM: Content is {type(content).__name__}, not str!")
        elif content.startswith('[File:'):
            print(f"\n❌ PROBLEM: Content starts with '[File:' - MALFORMED!")
        elif content.startswith('[['):
            print(f"\n❌ PROBLEM: Content starts with '[[' - MALFORMED!")
        else:
            print(f"\n✓ Content appears valid")

if __name__ == "__main__":
    inspect_chunks()
