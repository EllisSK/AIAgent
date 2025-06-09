import sys
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    exit(1)
else:
    prompt = str(sys.argv[1])
    #print(f"Prompt: {prompt}")

response = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
print(response.text)

input_tokens = response.usage_metadata.prompt_token_count
output_tokens = response.usage_metadata.candidates_token_count
print(f"Prompt tokens: {input_tokens}\nResponse tokens: {output_tokens}")
