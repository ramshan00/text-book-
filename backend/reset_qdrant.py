"""
Script to wipe Qdrant collection for a clean start
"""
import os
import sys
import logging
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def reset_qdrant():
    print("="*70)
    print("RESETTING QDRANT COLLECTION")
    print("="*70)
    
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = "rag_embedding"
    
    try:
        if qdrant_api_key and "localhost" not in qdrant_url:
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            print(f"✓ Connected to cloud Qdrant: {qdrant_url}")
        else:
            client = QdrantClient(path="./qdrant_data")
            print(f"✓ Connected to local Qdrant")
            
        # Check if collection exists
        collections = client.get_collections()
        exists = any(col.name == collection_name for col in collections.collections)
        
        if exists:
            # Delete collection
            print(f"\nDeleting collection '{collection_name}'...")
            client.delete_collection(collection_name=collection_name)
            print(f"✓ Collection '{collection_name}' DELETED successfully.")
        else:
            print(f"\nCollection '{collection_name}' does not exist (already clean).")
            
        print("\nReady for fresh embedding!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    reset_qdrant()
