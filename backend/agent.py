import os
import json
import logging
from typing import Dict, List
import time

# Optional: load local .env for secrets if running locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Transformers imports
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    logger.info("Transformers imported successfully")
except ImportError:
    raise ImportError("Please install transformers and torch: pip install transformers torch")

# Qdrant / RAG retriever import
try:
    from retrieving import RAGRetriever
except ImportError:
    logger.warning("RAGRetriever not found, make sure retrieving.py exists")

# --- Retrieval function ---
def retrieve_information(query: str) -> Dict:
    retriever = RAGRetriever()
    try:
        json_response = retriever.retrieve(query_text=query, top_k=5, threshold=0.3)
        results = json.loads(json_response)
        formatted_results = [
            {
                'content': chunk['content'],
                'url': chunk['url'],
                'position': chunk['position'],
                'similarity_score': chunk['similarity_score']
            }
            for chunk in results.get('results', [])
        ]
        return {
            'query': query,
            'retrieved_chunks': formatted_results,
            'total_results': len(formatted_results)
        }
    except Exception as e:
        logger.error(f"Error in retrieve_information: {e}")
        return {
            'query': query,
            'retrieved_chunks': [],
            'total_results': 0,
            'error': str(e)
        }

# --- RAG Agent class ---
class RAGAgent:
    def __init__(self):
        self.model_name = "google/flan-t5-base"  # Load locally instead of hosted API
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading Hugging Face model {self.model_name} on {self.device}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(self.device)
        logger.info("Model loaded successfully")

    def _sanitize_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Sanitize retrieved chunks to ensure they contain valid, substantive content.
        Filters out malformed chunks, metadata-only text, and low-quality content.
        """
        sanitized = []
        skipped_count = 0
        
        # Metadata patterns to filter out
        metadata_patterns = [
            'edit this page',
            'on this page',
            'table of contents',
            'previous next',
            'skip to content',
            'resources resources',
            'glossary glossary'
        ]
        
        for i, chunk in enumerate(chunks):
            content = chunk.get('content', '')
            
            # Validate content is a non-empty string
            if not content or not isinstance(content, str):
                logger.warning(f"Skipping chunk {i+1}: empty or non-string content (type: {type(content).__name__})")
                skipped_count += 1
                continue
            
            # Check for malformed content markers
            content_stripped = content.strip()
            if not content_stripped:
                logger.warning(f"Skipping chunk {i+1}: content is whitespace only")
                skipped_count += 1
                continue
            
            # Filter out chunks that start with common malformed patterns
            if content_stripped.startswith('[File:') or content_stripped.startswith('[['):
                logger.warning(f"Skipping chunk {i+1}: malformed content pattern detected: {content_stripped[:50]}...")
                skipped_count += 1
                continue
            
            # Filter out very short chunks (likely metadata or navigation)
            if len(content_stripped) < 100:
                logger.warning(f"Skipping chunk {i+1}: too short ({len(content_stripped)} chars) - likely metadata")
                skipped_count += 1
                continue
            
            # Filter out metadata-only chunks
            content_lower = content_stripped.lower()
            is_metadata = any(pattern in content_lower for pattern in metadata_patterns)
            if is_metadata and len(content_stripped) < 200:
                logger.warning(f"Skipping chunk {i+1}: appears to be metadata/navigation only")
                skipped_count += 1
                continue
            
            # Chunk is valid and substantive, keep it
            sanitized.append(chunk)
        
        if skipped_count > 0:
            logger.info(f"Sanitized chunks: kept {len(sanitized)}/{len(chunks)} (skipped {skipped_count} low-quality)")
        
        return sanitized

    def _build_prompt(self, query: str, retrieved_chunks: List[Dict]) -> str:
        """
        Build the prompt for the model using sanitized retrieved chunks.
        Optimized for T5 model format (512 token limit).
        """
        # Sanitize chunks before building prompt
        sanitized_chunks = self._sanitize_chunks(retrieved_chunks)
        
        if sanitized_chunks:
            # Build context from sanitized chunks
            # STRICT LIMITS: T5-base has 512 token limit (~2000 chars)
            # 3 chunks * 300 chars = 900 chars + overhead ~ 200 chars = ~1100 chars (safe)
            
            context_parts = []
            for i, chunk in enumerate(sanitized_chunks[:3], 1):
                content = chunk['content'][:250]
                context_parts.append(f"Context {i}: {content}")
            
            context = "\n\n".join(context_parts)
            
            # Put Question FIRST so it's never truncated
            prompt = f"""Question: {query}

Context:
{context}

Answer the question based on the context above. Provide a detailed answer.

Answer:"""
        else:
            if retrieved_chunks:
                # Had chunks but all were filtered out
                logger.warning("All retrieved chunks were filtered out during sanitization")
            # Fallback when no context available
            prompt = f"""Question: {query}

Answer: I don't have specific information about this topic in my knowledge base. Please ask about ROS 2, humanoid robotics, VLA systems, or simulation techniques."""
        
        return prompt

    def query_agent(self, query_text: str) -> Dict:
        start_time = time.time()
        try:
            # Retrieve chunks from Qdrant
            retrieval_result = retrieve_information(query_text)
            retrieved_chunks = retrieval_result.get('retrieved_chunks', [])
            
            # Log retrieval results
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query: '{query_text[:50]}...'")
            
            if len(retrieved_chunks) == 0:
                logger.warning("⚠ No chunks retrieved from Qdrant! Possible causes:")
                logger.warning("  1. Qdrant collection 'rag_embedding' is empty")
                logger.warning("  2. Similarity threshold is too high")
                logger.warning("  3. Query embedding generation failed")
                logger.warning("  → Run 'python debug_rag.py' to diagnose the issue")
            
            prompt = self._build_prompt(query_text, retrieved_chunks)
            
            # Log prompt for debugging
            logger.info(f"Prompt length: {len(prompt)} chars")
            logger.debug(f"Prompt preview: {prompt[:200]}...")

            # Tokenize and generate
            # Note: T5 models don't support temperature/top_p in generate()
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=3
            )
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Log generated answer for debugging
            logger.info(f"Generated answer length: {len(answer)} chars")
            logger.debug(f"Answer preview: {answer[:200]}...")

            sources = list({chunk['url'] for chunk in retrieved_chunks})
            query_time_ms = (time.time() - start_time) * 1000

            return {
                "answer": answer.strip(),
                "sources": sources,
                "matched_chunks": retrieved_chunks,
                "query_time_ms": query_time_ms,
                "confidence": self._calculate_confidence(retrieved_chunks),
                "status": "success"
            }

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            logger.error(f"Error processing query: {repr(e)}\n{error_details}")
            return {
                "answer": f"Error: {type(e).__name__} - {str(e)}",
                "sources": [],
                "matched_chunks": [],
                "error": f"{type(e).__name__}: {str(e)}",
                "query_time_ms": (time.time() - start_time) * 1000,
                "status": "error"
            }

    def _calculate_confidence(self, matched_chunks: List[Dict]) -> str:
        if not matched_chunks:
            return "low"
        avg_score = sum(c.get('similarity_score', 0.0) for c in matched_chunks) / len(matched_chunks)
        if avg_score >= 0.7:
            return "high"
        elif avg_score >= 0.4:
            return "medium"
        return "low"

# Convenience function
def query_agent_func(query_text: str) -> Dict:
    agent = RAGAgent()
    return agent.query_agent(query_text)

# --- Main test ---
if __name__ == "__main__":
    agent = RAGAgent()
    query = "What is ROS2?"
    response = agent.query_agent(query)
    print(f"Answer: {response['answer']}")
    print(f"Sources: {', '.join(response['sources'])}")
    print(f"Query time: {response['query_time_ms']:.2f}ms")
    print(f"Confidence: {response['confidence']}")
