"""
Script to check prompt token length and truncation
"""
import os
import sys
from transformers import AutoTokenizer

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_token_length():
    print("="*70)
    print("CHECKING PROMPT TOKEN LENGTH")
    print("="*70)
    
    model_name = "google/flan-t5-base"
    print(f"Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Simulate current prompt items
    # 5 chunks of 600 chars each
    chunk_text = "x" * 600
    chunks = [chunk_text for _ in range(5)]
    
    query = "What is ROS2? " * 5 # slightly longer query
    
    # Build prompt as in agent.py
    context_parts = []
    for i, content in enumerate(chunks, 1):
        context_parts.append(f"Context {i}: {content}")
    
    context = "\n\n".join(context_parts)
    
    prompt = f"""Answer the question based on the context below. Provide a detailed, informative answer.

Context:
{context}

Question: {query}

Answer:"""
    
    print(f"\nTotal Prompt Char Length: {len(prompt)}")
    
    # Check tokens
    tokens = tokenizer(prompt, return_tensors="pt")
    input_ids = tokens.input_ids[0]
    
    print(f"Total Token Count: {len(input_ids)}")
    
    if len(input_ids) > 512:
        print("\n❌ PROBLEM: Exceeds 512 token limit!")
        
        # Check truncation
        truncated = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        truncated_ids = truncated.input_ids[0]
        decoded = tokenizer.decode(truncated_ids)
        
        print("\n--- WHAT THE MODEL SEES (Decoded Truncated Input) ---")
        print(decoded[-200:]) # Print last 200 chars
        print("-----------------------------------------------------")
        
        if query not in decoded:
            print("\n❌ CRITICAL: The QUESTION is being truncated!")
            print("   The model sees context but NO question at the end.")
        else:
            print("\n✓ Question is present (barely?)")
            
    else:
        print("\n✓ Prompt fits within limit.")

if __name__ == "__main__":
    check_token_length()
