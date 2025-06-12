#Imports
import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

#System prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

#Connecting to the Gemini API
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

#CLI args parser set-up / flow control
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

#Setting up messages to send to model
messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

#Function calling schema
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to get the content of, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file at the specified file path replacing any existing file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to be written, relative to the working directory.",
            ),
            "content" : types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file.",
                ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file at a specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python file to run, relative to the working directory.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

#Getting a response from the model
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
)

#Usage statistics
input_tokens = response.usage_metadata.prompt_token_count
output_tokens = response.usage_metadata.candidates_token_count

#Output logic / flow control
if verbose == True:
    print(f"User prompt: {prompt}\n")
    print(f"Model output: {response.text}\n")
    if response.function_calls:
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
    print(f"Prompt tokens: {input_tokens}\n")
    print(f"Response tokens: {output_tokens}\n")
else:
    print(f"Model output: {response.text}\n")
    if response.function_calls:
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
