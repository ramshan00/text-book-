"""
Script to check prompt token length with FINAL LOGIC (3x300 chars)
"""
import os
import sys
from transformers import AutoTokenizer

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_final_logic():
    print("="*70)
    print("CHECKING FINAL PROMPT LOGIC (3x300 chars)")
    print("="*70)
    
    model_name = "google/flan-t5-base"
    print(f"Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Simulate FINAL logic: 3 chunks, 300 chars max
    chunk_text = "x" * 300
    chunks = [chunk_text for _ in range(3)]
    
    query = "What is ROS2? " * 5 
    
    context_parts = []
    for i, content in enumerate(chunks, 1):
        context_parts.append(f"Context {i}: {content}")
    
    context = "\n\n".join(context_parts)
    
    # Question FIRST
    prompt = f"""Question: {query}

Context:
{context}

Answer the question based on the context above. Provide a detailed answer.

Answer:"""
    
    print(f"\nTotal Prompt Char Length: {len(prompt)}")
    
    tokens = tokenizer(prompt, return_tensors="pt")
    input_ids = tokens.input_ids[0]
    
    print(f"Total Token Count: {len(input_ids)}")
    
    if len(input_ids) > 512:
        print("\n❌ PROBLEM: Still exceeds 512 token limit!")
    else:
        print("\n✅ SUCCESS: Fits comfortably within 512 token limit.")

if __name__ == "__main__":
    check_final_logic()
