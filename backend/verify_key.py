import os
from dotenv import load_dotenv
import openai

load_dotenv()
key = os.getenv('OPENAI_API_KEY')

print(f"Checking key: {key[:10]}...")

client = openai.OpenAI(api_key=key)

try:
    client.models.list()
    print("STATUS: VALID")
except Exception as e:
    print(f"STATUS: ERROR - {e}")
