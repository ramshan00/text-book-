import os
import json
import logging
from typing import Dict, List, Any
from dotenv import load_dotenv
import time

# Load environment variables FIRST before other imports
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Hugging Face
try:
    from huggingface_hub import InferenceClient
    logger.info("Hugging Face Hub imported successfully")
except ImportError:
    logger.error("huggingface_hub not installed. Run: pip install huggingface_hub")
    raise

def retrieve_information(query: str) -> Dict:
    """
    Retrieve information from the knowledge base based on a query
    """
    from retrieving import RAGRetriever
    retriever = RAGRetriever()

    try:
        # Call the existing retrieve method from the RAGRetriever instance
        json_response = retriever.retrieve(query_text=query, top_k=5, threshold=0.3)
        results = json.loads(json_response)

        # Format the results for the assistant
        formatted_results = []
        for result in results.get('results', []):
            formatted_results.append({
                'content': result['content'],
                'url': result['url'],
                'position': result['position'],
                'similarity_score': result['similarity_score']
            })

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

class RAGAgent:
    def __init__(self):
        # Get Hugging Face configuration
        self.hf_token = os.getenv("HUGGINGFACE_API_KEY")
        self.model = os.getenv("HUGGINGFACE_MODEL", "HuggingFaceH4/zephyr-7b-beta")
        
        if not self.hf_token:
            logger.error("HUGGINGFACE_API_KEY not set in environment variables")
            raise ValueError("HUGGINGFACE_API_KEY is required")
        
        logger.info(f"HUGGINGFACE_API_KEY is set (starts with {self.hf_token[:7]}...)")
        
        # Initialize Hugging Face Inference Client
        self.client = InferenceClient(token=self.hf_token)
        
        logger.info(f"RAG Agent initialized with Hugging Face model: {self.model}")

    def _build_prompt(self, query: str, retrieved_chunks: List[Dict]) -> str:
        """
        Build a prompt with system instructions, retrieved context, and user query
        """
        # System instructions
        prompt = """You are a helpful AI assistant that answers questions based on retrieved documents about Physical AI and Humanoid Robotics.

"""
        
        # Add retrieved context
        if retrieved_chunks and len(retrieved_chunks) > 0:
            prompt += "Context from knowledge base:\n\n"
            for i, chunk in enumerate(retrieved_chunks, 1):
                prompt += f"[Source {i} - {chunk['url']}]\n"
                prompt += f"{chunk['content']}\n\n"
            
            prompt += f"User Question: {query}\n\n"
            prompt += "Instructions: Answer the question based on the provided context above. "
            prompt += "If the context contains relevant information, use it to provide a detailed answer. "
            prompt += "Always mention which sources you used. "
            prompt += "If the context doesn't contain enough information, say so honestly.\n\n"
            prompt += "Answer:"
        else:
            prompt += f"User Question: {query}\n\n"
            prompt += "Note: No relevant documents were found in the knowledge base. "
            prompt += "Please provide a general answer or indicate that you don't have specific information.\n\n"
            prompt += "Answer:"
        
        return prompt

    def query_agent(self, query_text: str) -> Dict:
        """
        Process a query through the RAG agent and return structured response
        """
        start_time = time.time()

        logger.info(f"Processing query through RAG agent: '{query_text[:50]}...'")

        try:
            # Step 1: Retrieve relevant documents
            retrieval_result = retrieve_information(query_text)
            retrieved_chunks = retrieval_result.get('retrieved_chunks', [])
            
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks from knowledge base")

            # Step 2: Build prompt with context
            prompt = self._build_prompt(query_text, retrieved_chunks)
            
            logger.info(f"Built prompt with {len(retrieved_chunks)} context chunks")

            # Step 3: Call Hugging Face model using chat_completion
            logger.info(f"Calling Hugging Face model: {self.model}")
            
            # Format as chat messages for better compatibility
            messages = [{"role": "user", "content": prompt}]
            
            response = self.client.chat_completion(
                messages=messages,
                model=self.model,
                max_tokens=512,
                temperature=0.7,
                top_p=0.95
            )
            
            # Extract the response text
            answer = response.choices[0].message.content
            
            logger.info(f"Received response from Hugging Face")

            # Step 4: Extract sources
            sources = list(set([chunk['url'] for chunk in retrieved_chunks]))
            
            # Step 5: Calculate query time
            query_time_ms = (time.time() - start_time) * 1000

            # Step 6: Format response
            result = {
                "answer": answer.strip(),
                "sources": sources,
                "matched_chunks": retrieved_chunks,
                "query_time_ms": query_time_ms,
                "confidence": self._calculate_confidence(retrieved_chunks)
            }

            logger.info(f"Query processed in {query_time_ms:.2f}ms")
            return result

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "answer": f"Sorry, I encountered an error: {str(e)}",
                "sources": [],
                "matched_chunks": [],
                "error": str(e),
                "query_time_ms": (time.time() - start_time) * 1000
            }

    def _calculate_confidence(self, matched_chunks: List[Dict]) -> str:
        """
        Calculate confidence level based on similarity scores and number of matches
        """
        if not matched_chunks:
            return "low"

        avg_score = sum(chunk.get('similarity_score', 0.0) for chunk in matched_chunks) / len(matched_chunks)

        if avg_score >= 0.7:
            return "high"
        elif avg_score >= 0.4:
            return "medium"
        else:
            return "low"

def query_agent(query_text: str) -> Dict:
    """
    Convenience function to query the RAG agent
    """
    agent = RAGAgent()
    return agent.query_agent(query_text)

def main():
    """
    Main function to demonstrate the RAG agent functionality
    """
    logger.info("Initializing RAG Agent...")

    # Initialize the agent
    agent = RAGAgent()

    # Example queries to test the system
    test_queries = [
        "What is ROS2?",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"Query {i}: {query}")
        print('='*60)
        
        # Process query through agent
        response = agent.query_agent(query)
        
        print(f"\nAnswer: {response['answer']}")
        print(f"\nSources: {', '.join(response['sources'])}")
        print(f"Query time: {response['query_time_ms']:.2f}ms")
        print(f"Confidence: {response['confidence']}")

if __name__ == "__main__":
    main()