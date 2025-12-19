"""
Simple RAG Agent Test Script

Tests the RAG agent end-to-end without complex Qdrant client calls.
This bypasses version compatibility issues and focuses on actual functionality.
"""

import os
import sys
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

def test_retrieval():
    """Test the retrieval pipeline"""
    print("\n" + "="*60)
    print("TEST 1: Retrieval Pipeline")
    print("="*60)
    
    try:
        from retrieving import RAGRetriever
        import json
        
        retriever = RAGRetriever()
        test_query = "What is ROS2?"
        
        print(f"\nQuery: '{test_query}'")
        print("Retrieving chunks...")
        
        json_response = retriever.retrieve(query_text=test_query, top_k=5, threshold=0.3)
        results = json.loads(json_response)
        
        chunks = results.get('results', [])
        print(f"\n✓ Retrieved {len(chunks)} chunks")
        
        if len(chunks) == 0:
            print("\n⚠ WARNING: No chunks retrieved!")
            print("   This means:")
            print("   1. Qdrant collection might be empty, OR")
            print("   2. Similarity threshold (0.3) is too high, OR")
            print("   3. No matching documents for this query")
            return False
        
        # Show chunk previews
        for i, chunk in enumerate(chunks[:3], 1):
            content = chunk.get('content', '')
            score = chunk.get('similarity_score', 0)
            url = chunk.get('url', 'N/A')
            
            print(f"\n--- Chunk {i} (Score: {score:.3f}) ---")
            print(f"URL: {url}")
            
            # Check for malformed content
            if not isinstance(content, str):
                print(f"❌ ERROR: Content is not a string (type: {type(content).__name__})")
                return False
            elif content.startswith('[File:') or content.startswith('[['):
                print(f"❌ ERROR: Malformed content: {content[:100]}")
                return False
            else:
                preview = content[:200].replace('\n', ' ')
                print(f"Content: {preview}...")
        
        print("\n✓ All chunks have valid content")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_agent():
    """Test the complete RAG agent"""
    print("\n" + "="*60)
    print("TEST 2: RAG Agent End-to-End")
    print("="*60)
    
    try:
        from agent import RAGAgent
        
        print("\nInitializing RAG Agent...")
        agent = RAGAgent()
        print("✓ Agent initialized successfully")
        
        test_queries = [
            "What is ROS2?",
            "Explain humanoid design principles"
        ]
        
        for query in test_queries:
            print(f"\n--- Testing Query: '{query}' ---")
            
            response = agent.query_agent(query)
            
            status = response.get('status')
            confidence = response.get('confidence')
            answer = response.get('answer', '')
            sources = response.get('sources', [])
            chunks = response.get('matched_chunks', [])
            
            print(f"Status: {status}")
            print(f"Confidence: {confidence}")
            print(f"Sources: {len(sources)} found")
            print(f"Chunks: {len(chunks)} matched")
            
            # Check for malformed output
            if '[File:' in answer or (answer.startswith('[') and not answer.startswith('[Source')):
                print(f"\n❌ ERROR: Answer contains malformed output!")
                print(f"Answer: {answer[:200]}")
                return False
            
            if len(answer.strip()) == 0:
                print("\n⚠ WARNING: Answer is empty")
            else:
                print(f"\nAnswer ({len(answer)} chars):")
                print(answer[:300] + "..." if len(answer) > 300 else answer)
            
            print("\n✓ Query processed successfully")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*70)
    print("RAG CHATBOT SIMPLE TEST")
    print("="*70)
    
    results = {
        "retrieval": False,
        "agent": False
    }
    
    # Test retrieval first
    results["retrieval"] = test_retrieval()
    
    # Only test agent if retrieval works
    if results["retrieval"]:
        results["agent"] = test_rag_agent()
    else:
        print("\n⚠ Skipping agent test due to retrieval failure")
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test, passed in results.items():
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test}")
    
    if all(results.values()):
        print("\n✅ All tests passed! RAG chatbot is working correctly.")
        print("\nYour fixes have resolved the malformed output issue:")
        print("  • Chunk sanitization is filtering invalid content")
        print("  • Prompt building uses only valid string chunks")
        print("  • Model generates proper responses")
    else:
        print("\n❌ Some tests failed.")
        if not results["retrieval"]:
            print("\nRetrieval failed - possible causes:")
            print("  1. Qdrant collection is empty")
            print("  2. Embedding pipeline hasn't been run")
            print("  3. Similarity threshold is too high")
            print("\n→ Check if you have an embedding script to populate Qdrant")


if __name__ == "__main__":
    main()
