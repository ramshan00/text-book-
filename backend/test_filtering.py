"""
Test the improved chunk filtering and answer quality
"""

import os
import sys
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

def test_answer_quality():
    """Test that answers are detailed and not fragmented"""
    print("="*70)
    print("TESTING ANSWER QUALITY WITH IMPROVED FILTERING")
    print("="*70)
    
    from retrieving import RAGRetriever
    import json
    
    retriever = RAGRetriever()
    
    # Test queries
    test_queries = [
        "What is ROS2?",
        "hello",
        "Explain humanoid design"
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Query: '{query}'")
        print(f"{'='*70}")
        
        # Get raw retrieval results
        json_response = retriever.retrieve(query_text=query, top_k=5, threshold=0.0)
        results = json.loads(json_response)
        chunks = results.get('results', [])
        
        print(f"\nRetrieved {len(chunks)} chunks:")
        
        # Show what would be filtered
        from agent import RAGAgent
        agent_instance = RAGAgent.__new__(RAGAgent)  # Create without __init__
        
        # Manually call sanitization
        sanitized = []
        metadata_patterns = [
            'edit this page', 'on this page', 'table of contents',
            'previous next', 'skip to content', 'resources resources',
            'glossary glossary'
        ]
        
        for i, chunk in enumerate(chunks, 1):
            content = chunk.get('content', '').strip()
            score = chunk.get('similarity_score', 0)
            
            # Check filters
            too_short = len(content) < 100
            is_metadata = any(p in content.lower() for p in metadata_patterns) and len(content) < 200
            
            status = "✓ KEEP" if not (too_short or is_metadata) else "✗ SKIP"
            reason = ""
            if too_short:
                reason = f"(too short: {len(content)} chars)"
            elif is_metadata:
                reason = "(metadata only)"
            
            print(f"  {status} Chunk {i} - Score: {score:.3f} {reason}")
            print(f"       Content: {content[:100]}...")
            
            if not (too_short or is_metadata):
                sanitized.append(chunk)
        
        print(f"\n→ After filtering: {len(sanitized)} substantive chunks")
        
        if len(sanitized) == 0:
            print("⚠ WARNING: All chunks filtered out - answer will be generic")

if __name__ == "__main__":
    test_answer_quality()
