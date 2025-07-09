import os

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