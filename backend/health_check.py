#!/usr/bin/env python3
"""
Backend API Health Check Script
Tests connectivity to Qdrant, OpenAI, and Cohere services
"""
import os
import sys
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def check_env_variables():
    """Check if required environment variables are set"""
    logger.info("=" * 60)
    logger.info("CHECKING ENVIRONMENT VARIABLES")
    logger.info("=" * 60)
    
    required_vars = {
        'COHERE_API_KEY': 'Cohere API Key',
        'HUGGINGFACE_API_KEY': 'Hugging Face API Key',
        'QDRANT_URL': 'Qdrant URL',
    }
    
    optional_vars = {
        'QDRANT_API_KEY': 'Qdrant API Key (optional for local)',
        'HUGGINGFACE_MODEL': 'Hugging Face Model (optional)',
    }
    
    all_good = True
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Show first 10 chars for security
            masked = value[:10] + "..." if len(value) > 10 else value
            logger.info(f"✓ {description}: {masked}")
        else:
            logger.error(f"✗ {description}: NOT SET")
            all_good = False
    
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            masked = value[:10] + "..." if len(value) > 10 else value
            logger.info(f"✓ {description}: {masked}")
        else:
            logger.info(f"○ {description}: Not set (optional)")
    
    return all_good

def check_qdrant():
    """Check Qdrant connectivity"""
    logger.info("\n" + "=" * 60)
    logger.info("CHECKING QDRANT CONNECTIVITY")
    logger.info("=" * 60)
    
    try:
        from qdrant_client import QdrantClient
        
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        logger.info(f"Connecting to Qdrant at: {qdrant_url}")
        
        if qdrant_api_key:
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            client = QdrantClient(url=qdrant_url)
        
        # Try to get collections
        collections = client.get_collections()
        logger.info(f"✓ Successfully connected to Qdrant")
        logger.info(f"  Collections found: {len(collections.collections)}")
        
        for col in collections.collections:
            logger.info(f"    - {col.name}")
        
        # Check if rag_embedding collection exists
        collection_names = [col.name for col in collections.collections]
        if "rag_embedding" in collection_names:
            logger.info(f"✓ 'rag_embedding' collection exists")
            
            # Get collection info
            info = client.get_collection("rag_embedding")
            logger.info(f"  Vector count: {info.points_count}")
            logger.info(f"  Vector size: {info.config.params.vectors.size}")
        else:
            logger.warning(f"⚠ 'rag_embedding' collection does NOT exist")
            logger.info(f"  Run 'python main.py' to create and populate it")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to connect to Qdrant: {e}")
        logger.info(f"  Make sure Qdrant is running at {qdrant_url}")
        return False

def check_cohere():
    """Check Cohere API connectivity"""
    logger.info("\n" + "=" * 60)
    logger.info("CHECKING COHERE API CONNECTIVITY")
    logger.info("=" * 60)
    
    try:
        import cohere
        
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            logger.error("✗ COHERE_API_KEY not set")
            return False
        
        client = cohere.Client(api_key=api_key)
        
        # Test with a simple embedding
        logger.info("Testing embedding generation...")
        response = client.embed(
            texts=["test"],
            model="embed-multilingual-v3.0",
            input_type="search_query"
        )
        
        logger.info(f"✓ Successfully connected to Cohere API")
        logger.info(f"  Embedding dimension: {len(response.embeddings[0])}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to connect to Cohere API: {e}")
        return False

def check_huggingface():
    """Check Hugging Face API connectivity"""
    logger.info("\n" + "=" * 60)
    logger.info("CHECKING HUGGING FACE API CONNECTIVITY")
    logger.info("=" * 60)
    
    try:
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            logger.error("✗ HUGGINGFACE_API_KEY not set")
            return False
        
        model = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
        
        from huggingface_hub import InferenceClient
        
        client = InferenceClient(token=api_key)
        
        # Test with a simple text generation
        logger.info(f"Testing text generation with model: {model}")
        response = client.text_generation(
            "Hello",
            model=model,
            max_new_tokens=10
        )
        
        logger.info(f"✓ Successfully connected to Hugging Face API")
        logger.info(f"  Model: {model}")
        logger.info(f"  Test response: {response[:50]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to connect to Hugging Face API: {e}")
        return False

def main():
    """Run all health checks"""
    logger.info("\n" + "=" * 60)
    logger.info("BACKEND API HEALTH CHECK")
    logger.info("=" * 60 + "\n")
    
    results = {
        'Environment Variables': check_env_variables(),
        'Qdrant': check_qdrant(),
        'Cohere': check_cohere(),
        'Hugging Face': check_huggingface(),
    }
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("HEALTH CHECK SUMMARY")
    logger.info("=" * 60)
    
    for service, status in results.items():
        status_icon = "✓" if status else "✗"
        status_text = "PASS" if status else "FAIL"
        logger.info(f"{status_icon} {service}: {status_text}")
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("\n✓ All health checks passed! Backend is ready to run.")
        logger.info("\nTo start the backend API server:")
        logger.info("  cd backend")
        logger.info("  python api.py")
        return 0
    else:
        logger.error("\n✗ Some health checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
