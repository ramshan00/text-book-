"""
Script to check prompt token length with NEW FIXED LOGIC
"""
import os
import sys
from transformers import AutoTokenizer

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_new_logic():
    print("="*70)
    print("CHECKING FIXED PROMPT LOGIC")
    print("="*70)
    
    model_name = "google/flan-t5-base"
    print(f"Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Simulate NEW logic: 3 chunks, 450 chars max
    chunk_text = "x" * 450
    chunks = [chunk_text for _ in range(3)]
    
    query = "What is ROS2? " * 5 
    
    context_parts = []
    for i, content in enumerate(chunks, 1):
        context_parts.append(f"Context {i}: {content}")
    
    context = "\n\n".join(context_parts)
    
    # NEW PROMPT FORMAT: Question FIRST
    prompt = f"""Question: {query}

Context:
{context}

Answer the question based on the context above. Provide a detailed answer.

Answer:"""
    
    print(f"\nTotal Prompt Char Length: {len(prompt)}")
    
    tokens = tokenizer(prompt, return_tensors="pt")
    input_ids = tokens.input_ids[0]
    
    print(f"Total Token Count: {len(input_ids)}")
    
    if len(input_ids) > 512 + 50: # Allow slight buffer for special tokens
        print("\n⚠ WARNING: Approaching limit, but checking content...")
    else:
        print("\n✓ Fits comfortably within limit.")
        
    # Check truncation just in case
    truncated = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    truncated_ids = truncated.input_ids[0]
    decoded = tokenizer.decode(truncated_ids)
    
    print("\n--- WHAT THE MODEL SEES (Decoded Truncated Input) ---")
    print(decoded[:200]) # Print FIRST 200 chars (Question should be here)
    print("...")
    print(decoded[-200:]) # Print LAST 200 chars
    print("-----------------------------------------------------")
    
    if query in decoded[:500]:
        print("\n✅ SUCCESS: The QUESTION is present at the START!")
    else:
        print("\n❌ CRITICAL: Question NOT found at start!")

if __name__ == "__main__":
    check_new_logic()
