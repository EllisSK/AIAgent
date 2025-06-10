import os

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)

    if file_path:
        target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_path.startswith(abs_working_dir):
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(target_file_path):
        return (f'Error: File not found or is not a regular file: "{file_path}"')
    
    MAX_CHARACTERS = 10000

    try:
        with open(target_file_path, "r") as f:
            file_contents_string = f.read(MAX_CHARACTERS)
            
        if len(file_contents_string) == MAX_CHARACTERS:
            file_contents_string += f'[...File "{file_path}" truncated at 10000 characters]'
        
        return file_contents_string
    
    except Exception as e:
        return f"Error: {e}"
