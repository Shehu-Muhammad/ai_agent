import os
from functions.config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    if abs_full_path.startswith(abs_working_directory):
        if os.path.isfile(full_path):
            try:
                with open(full_path, "r") as f:
                    file_content_string = f.read(MAX_CHARS)
                    if f.read(1) == "":
                        return file_content_string
                    else:
                        return file_content_string + f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'
            except Exception as e:
                return f'Error: {e}'
        else:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents in the specified directory along with whether the file was truncated, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that will be read and/or truncated.",
            ),
        },
        required=["file_path"],
    ),
)