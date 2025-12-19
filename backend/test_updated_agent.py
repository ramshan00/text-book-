"""
Test the updated agent with fixed generation parameters
"""

import os
import sys
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

def test_updated_agent():
    """Test agent with new prompt format and generation params"""
    print("="*70)
    print("TESTING UPDATED RAG AGENT")
    print("="*70)
    
    try:
        from agent import RAGAgent
        
        print("\nInitializing agent...")
        agent = RAGAgent()
        print("✓ Agent initialized\n")
        
        # Test with same query from production
        test_query = "hello"
        
        print(f"Query: '{test_query}'")
        print("-"*70)
        
        response = agent.query_agent(test_query)
        
        answer = response.get('answer', '')
        status = response.get('status')
        confidence = response.get('confidence')
        sources = response.get('sources', [])
        
        print(f"\nStatus: {status}")
        print(f"Confidence: {confidence}")
        print(f"Sources: {len(sources)}")
        print(f"\nAnswer ({len(answer)} chars):")
        print("="*70)
        print(answer)
        print("="*70)
        
        # Check for malformed output
        if '[File:' in answer:
            print("\n❌ ERROR: Answer still contains '[File:' pattern!")
            return False
        elif answer.startswith('[['):
            print("\n❌ ERROR: Answer starts with '[[' pattern!")
            return False
        elif len(answer.strip()) == 0:
            print("\n⚠ WARNING: Answer is empty")
            return False
        else:
            print("\n✓ Answer appears valid (no malformed patterns detected)")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_updated_agent()
    
    if success:
        print("\n" + "="*70)
        print("✅ TEST PASSED - Agent is working correctly!")
        print("="*70)
        print("\nNext step: Deploy updated agent.py to Hugging Face Space")
    else:
        print("\n" + "="*70)
        print("❌ TEST FAILED - See errors above")
        print("="*70)
