"""
Final System Health Check Script
Verifies Data, Retrieval, and Prompt Logic
"""
import os
import sys
import json
import logging
from typing import List, Dict
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from transformers import AutoTokenizer

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Logging setup
logging.basicConfig(level=logging.ERROR) # Only show errors from libraries
logger = logging.getLogger(__name__)

load_dotenv()

def print_status(component, status, details=""):
    symbol = "✅" if status == "PASS" else "❌"
    print(f"{symbol} [{component:<15}] {status} {details}")

def check_qdrant_data():
    try:
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        if qdrant_api_key and "localhost" not in qdrant_url:
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            client = QdrantClient(path="./qdrant_data")
            
        # Use simpler check to avoid strict Pydantic validation errors on get_collection info
        collections = client.get_collections()
        exists = any(col.name == "rag_embedding" for col in collections.collections)
        
        if not exists:
            print_status("Qdrant Data", "FAIL", "Collection 'rag_embedding' not found!")
            return False, client
            
        # Check count using scroll/count API which is safer than get_collection logic
        count_result = client.count(collection_name="rag_embedding")
        count = count_result.count
        
        if count > 0:
            print_status("Qdrant Data", "PASS", f"Found {count} documents (Expected ~24)")
            return True, client
        else:
            print_status("Qdrant Data", "FAIL", "Collection is empty!")
            return False, client
            
    except Exception as e:
        print_status("Qdrant Data", "FAIL", f"Connection error: {str(e)}")
        return False, None

def check_retrieval():
    try:
        from retrieving import RAGRetriever
        retriever = RAGRetriever()
        query = "What is ROS2?"
        
        json_results = retriever.retrieve(query_text=query, top_k=5, threshold=0.0)
        results = json.loads(json_results)
        chunks = results.get('results', [])
        
        if len(chunks) > 0:
            print_status("Retrieval", "PASS", f"Retrieved {len(chunks)} chunks for '{query}'")
            return chunks
        else:
            print_status("Retrieval", "FAIL", "No chunks returned")
            return []
            
    except Exception as e:
        print_status("Retrieval", "FAIL", f"Error: {str(e)}")
        return []

def check_sanitization_and_prompt(chunks):
    try:
        # Simulate Agent Logic
        sanitized = []
        metadata_patterns = ['edit this page', 'on this page', 'resources resources']
        
        for chunk in chunks:
            content = chunk.get('content', '').strip()
            if len(content) < 100: continue
            if any(p in content.lower() for p in metadata_patterns) and len(content) < 200: continue
            sanitized.append(chunk)
            
        print_status("Sanitization", "PASS", f"Filtered {len(chunks)} -> {len(sanitized)} valid chunks")
        
        # Simulate Prompt Construction
        context_parts = []
        for i, chunk in enumerate(sanitized[:3], 1): # Top 3
            content = chunk['content'][:250]         # Max 250 chars
            context_parts.append(f"Context {i}: {content}")
        
        context = "\n\n".join(context_parts)
        query = "What is ROS2?"
        
        # New Prompt Format
        prompt = f"""Question: {query}

Context:
{context}

Answer the question based on the context above. Provide a detailed answer.

Answer:"""

        # Verify Token Limit
        model_name = "google/flan-t5-base"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids[0]
        token_count = len(input_ids)
        
        limit = 512
        status = "PASS" if token_count < limit else "FAIL"
        
        print_status("Prompt Safe", status, f"Token count: {token_count}/{limit} ({(token_count/limit)*100:.1f}%)")
        
        if status == "PASS":
            print("\n--- FINAL PROMPT PREVIEW (Model Input) ---")
            print(prompt[:300] + "...")
            print("------------------------------------------")
            
    except Exception as e:
        print_status("Prompt Logic", "FAIL", f"Error: {str(e)}")

def main():
    print("======================================================================")
    print("FINAL SYSTEM HEALTH CHECK")
    print("======================================================================")
    
    data_ok, client = check_qdrant_data()
    
    if data_ok:
        chunks = check_retrieval()
        if chunks:
            check_sanitization_and_prompt(chunks)
            
    print("======================================================================")

if __name__ == "__main__":
    main()
