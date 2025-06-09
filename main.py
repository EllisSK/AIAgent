import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser()
parser.add_argument("prompt", help= "Prompt text")
parser.add_argument("--verbose", action= "store_true", help= "Verbose output")
args = parser.parse_args()

if not args.prompt:
    exit(1)
elif args.verbose:
    verbose = True
    prompt = args.prompt
else:
    verbose = False
    prompt = args.prompt

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

input_tokens = response.usage_metadata.prompt_token_count
output_tokens = response.usage_metadata.candidates_token_count

if verbose == True:
    print(f"User prompt: {prompt}\n")
    print(f"Model output: {response.text}\n")
    print(f"Prompt tokens: {input_tokens}\n")
    print(f"Response tokens: {output_tokens}\n")
else:
    print(f"Model output: {response.text}\n")
