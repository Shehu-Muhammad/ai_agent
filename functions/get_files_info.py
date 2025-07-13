import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    if directory == None:
        full_path = os.path.abspath(working_directory)
    else:
        full_path = os.path.abspath(os.path.join(working_directory, directory))
    if full_path.startswith(abs_working_directory):
        if os.path.isdir(full_path):
            try:
                directory_items = os.listdir(full_path)
                info = []
                for item in directory_items:
                    item_path = os.path.join(full_path, item)
                    info.append(f'- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}')
                return '\n'.join(info)
            except Exception as e:
                return f'Error: {e}'
        else:
            return f'Error: "{directory}" is not a directory'
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
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