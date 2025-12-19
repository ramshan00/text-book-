"""
RAG Chatbot Debugging Script

This script helps diagnose and fix common issues with RAG chatbot output:
- Verifies Qdrant collection exists and has data
- Validates chunk content format
- Tests retrieval pipeline
- Provides detailed diagnostics
"""

import os
import sys
import json
import logging
from typing import Dict, List
from dotenv import load_dotenv

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_qdrant_collection():
    """Step 1: Verify Qdrant collection exists and has data"""
    print("\n" + "="*60)
    print("STEP 1: Checking Qdrant Collection")
    print("="*60)
    
    try:
        from qdrant_client import QdrantClient
        
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        # Initialize client
        if qdrant_api_key and "localhost" not in qdrant_url:
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            print(f"✓ Connected to Qdrant at: {qdrant_url}")
        else:
            client = QdrantClient(path="./qdrant_data")
            print(f"✓ Connected to local Qdrant at: ./qdrant_data")
        
        # Get all collections
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]
        
        print(f"\nAvailable collections: {collection_names}")
        
        # Check if rag_embedding exists
        if "rag_embedding" not in collection_names:
            print("\n❌ ERROR: Collection 'rag_embedding' does NOT exist!")
            print("   → You need to run your embedding pipeline to create the collection")
            print("   → Run: python embedding.py (or your embedding script)")
            return False
        
        print("✓ Collection 'rag_embedding' exists")
        
        # Get collection info
        collection_info = client.get_collection("rag_embedding")
        point_count = collection_info.points_count
        
        print(f"✓ Collection has {point_count} points (chunks)")
        
        if point_count == 0:
            print("\n❌ WARNING: Collection is EMPTY!")
            print("   → Run your embedding pipeline to populate the collection")
            return False
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR checking Qdrant: {e}")
        logger.error(f"Qdrant check failed: {e}", exc_info=True)
        return False


def validate_chunk_content():
    """Step 2: Validate retrieved chunks have proper content"""
    print("\n" + "="*60)
    print("STEP 2: Validating Chunk Content")
    print("="*60)
    
    try:
        from retrieving import RAGRetriever
        
        retriever = RAGRetriever()
        
        # Test query
        test_query = "What is ROS2?"
        print(f"\nTest query: '{test_query}'")
        
        # Retrieve chunks
        json_response = retriever.retrieve(query_text=test_query, top_k=5, threshold=0.3)
        results = json.loads(json_response)
        
        retrieved_chunks = results.get('results', [])
        
        print(f"\n✓ Retrieved {len(retrieved_chunks)} chunks")
        
        if len(retrieved_chunks) == 0:
            print("\n❌ WARNING: No chunks retrieved!")
            print("   → Possible causes:")
            print("      1. Collection is empty")
            print("      2. Threshold (0.3) is too high")
            print("      3. Query embedding failed")
            return False
        
        # Validate each chunk
        issues_found = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            print(f"\n--- Chunk {i} ---")
            print(f"URL: {chunk.get('url', 'MISSING')}")
            print(f"Score: {chunk.get('similarity_score', 0):.3f}")
            
            content = chunk.get('content', '')
            
            # Check for issues
            if not content:
                issues_found.append(f"Chunk {i}: Empty content")
                print("❌ Content: EMPTY")
            elif not isinstance(content, str):
                issues_found.append(f"Chunk {i}: Content is not a string (type: {type(content).__name__})")
                print(f"❌ Content type: {type(content).__name__} (should be str)")
            elif content.startswith('[File:') or content.startswith('['):
                issues_found.append(f"Chunk {i}: Content appears to be malformed (starts with '[File:' or '[')")
                print(f"❌ Content appears malformed: {content[:100]}")
            else:
                preview = content[:150].replace('\n', ' ')
                print(f"✓ Content preview: {preview}...")
        
        if issues_found:
            print("\n❌ ISSUES FOUND:")
            for issue in issues_found:
                print(f"   - {issue}")
            return False
        
        print("\n✓ All chunks have valid content")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR validating chunks: {e}")
        logger.error(f"Chunk validation failed: {e}", exc_info=True)
        return False


def test_prompt_building():
    """Step 3: Test prompt construction with sanitized chunks"""
    print("\n" + "="*60)
    print("STEP 3: Testing Prompt Building")
    print("="*60)
    
    try:
        from retrieving import RAGRetriever
        
        retriever = RAGRetriever()
        test_query = "What is ROS2?"
        
        # Retrieve chunks
        json_response = retriever.retrieve(query_text=test_query, top_k=3, threshold=0.3)
        results = json.loads(json_response)
        retrieved_chunks = results.get('results', [])
        
        print(f"\nRetrieved {len(retrieved_chunks)} chunks")
        
        # Sanitize chunks
        sanitized_chunks = []
        for chunk in retrieved_chunks:
            content = chunk.get('content', '')
            
            # Validate content is a proper string
            if content and isinstance(content, str) and len(content.strip()) > 0:
                # Remove any malformed markers
                if not content.startswith('[File:') and not content.startswith('['):
                    sanitized_chunks.append(chunk)
                else:
                    print(f"⚠ Skipping malformed chunk: {content[:50]}...")
        
        print(f"✓ Sanitized to {len(sanitized_chunks)} valid chunks")
        
        # Build prompt
        prompt = "You are a helpful AI assistant answering questions based on retrieved documents.\n\n"
        
        if sanitized_chunks:
            prompt += "Context from knowledge base:\n\n"
            for i, chunk in enumerate(sanitized_chunks, 1):
                prompt += f"[Source {i} - {chunk['url']}]\n{chunk['content']}\n\n"
            prompt += f"User Question: {test_query}\n\nAnswer:"
        else:
            prompt += f"User Question: {test_query}\n\nNo relevant documents found. Answer generally or indicate lack of info.\n\nAnswer:"
        
        print("\n--- Generated Prompt Preview (first 500 chars) ---")
        print(prompt[:500])
        print("...")
        
        print(f"\n✓ Prompt built successfully ({len(prompt)} characters)")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR building prompt: {e}")
        logger.error(f"Prompt building failed: {e}", exc_info=True)
        return False


def test_end_to_end():
    """Step 4: Test complete RAG agent flow"""
    print("\n" + "="*60)
    print("STEP 4: Testing End-to-End RAG Agent")
    print("="*60)
    
    try:
        from agent import RAGAgent
        
        print("\nInitializing RAG Agent...")
        agent = RAGAgent()
        print("✓ Agent initialized")
        
        test_query = "What is ROS2?"
        print(f"\nQuerying: '{test_query}'")
        
        response = agent.query_agent(test_query)
        
        print("\n--- Response ---")
        print(f"Status: {response.get('status')}")
        print(f"Confidence: {response.get('confidence')}")
        print(f"Query time: {response.get('query_time_ms', 0):.2f}ms")
        print(f"Sources: {response.get('sources', [])}")
        print(f"Matched chunks: {len(response.get('matched_chunks', []))}")
        
        answer = response.get('answer', '')
        print(f"\nAnswer ({len(answer)} chars):")
        print(answer)
        
        # Check for malformed output
        if '[File:' in answer or answer.startswith('['):
            print("\n❌ ERROR: Answer contains malformed output!")
            print("   → This indicates chunks are not being sanitized properly")
            return False
        
        if len(answer.strip()) == 0:
            print("\n❌ WARNING: Answer is empty!")
            return False
        
        print("\n✓ End-to-end test successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR in end-to-end test: {e}")
        logger.error(f"End-to-end test failed: {e}", exc_info=True)
        return False


def run_diagnostics():
    """Run all diagnostic checks"""
    print("\n" + "="*70)
    print("RAG CHATBOT DIAGNOSTIC TOOL")
    print("="*70)
    
    results = {
        "qdrant_check": False,
        "chunk_validation": False,
        "prompt_building": False,
        "end_to_end": False
    }
    
    # Run checks in sequence
    results["qdrant_check"] = check_qdrant_collection()
    
    if results["qdrant_check"]:
        results["chunk_validation"] = validate_chunk_content()
        results["prompt_building"] = test_prompt_building()
        results["end_to_end"] = test_end_to_end()
    else:
        print("\n⚠ Skipping remaining tests due to Qdrant issues")
    
    # Summary
    print("\n" + "="*70)
    print("DIAGNOSTIC SUMMARY")
    print("="*70)
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ All checks passed! Your RAG chatbot should work correctly.")
    else:
        print("\n❌ Some checks failed. Please review the errors above.")
        print("\nCommon fixes:")
        print("1. If Qdrant collection is missing/empty:")
        print("   → Run your embedding pipeline to populate the collection")
        print("2. If chunks are malformed:")
        print("   → Check your embedding script - ensure chunks are stored as plain text")
        print("3. If retrieval returns 0 results:")
        print("   → Lower the similarity threshold (currently 0.3)")
        print("   → Check that embeddings are being generated correctly")
    
    return all_passed


if __name__ == "__main__":
    run_diagnostics()
