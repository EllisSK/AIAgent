import os
import sys
import subprocess as sp

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File "{file_path}" not found.'
    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        process = sp.run([sys.executable, target_file_path], timeout= 30, capture_output=True, text=True)
        output_string = f'Ran\nSTDOUT: {process.stdout}\nSTDERR: {process.stderr}\n'

        if process.returncode != 0:
            output_string += f'Process exited with code {process.returncode}'
        if not process.stdout:
            return "No output produced."

        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
