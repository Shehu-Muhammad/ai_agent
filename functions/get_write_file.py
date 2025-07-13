import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    if abs_full_path.startswith(abs_working_directory):
        try:
            os.makedirs(os.path.dirname(abs_full_path), exist_ok=True)
            with open(abs_full_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f'Error: {e}'
    else:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the file if it is in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file file that content will be added to."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text that will be added to the file."    
            ),
        },
        required=["file_path", "content"],
    ),
)