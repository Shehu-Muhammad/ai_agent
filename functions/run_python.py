import os
import subprocess
import sys

def run_python_file(working_directory, file_path):
    # absolute_working_directory path
    abs_working_directory = os.path.abspath(working_directory)
    # full_path, working_directory joined with file_path
    full_path = os.path.join(working_directory, file_path)
    # absolute_full_path
    abs_full_path = os.path.abspath(full_path)

    # check if file_path is outside working directory
    if abs_full_path.startswith(abs_working_directory):
        # check if file_path doesn't exist
        if os.path.exists(abs_full_path):
            # check if file doesn't end with '.py'
            if abs_full_path.endswith('.py'):
                try:
                    # use subprocess.run to execute the python file
                    # set a timeout of 30 seconds to prevent infinite execution
                    # capture both stdout and stderr
                    # set the working directory properly
                    result = subprocess.run([sys.executable, abs_full_path], capture_output=True, timeout=30, cwd=abs_working_directory)
                    stdout = result.stdout.decode()
                    stderr = result.stderr.decode()
                    # if no output was produced
                    if not stdout and not stderr:
                        return "No output produced."
                    output = f"STDOUT:{stdout}\nSTDERR:{stderr}"
                    # if process exits with a non-zero code, include "Process exited with code X"
                    if result.returncode != 0:
                        output += f"\nProcess exited with code {result.returncode}"
                    # if process exits with a zero code
                    return output
                except Exception as e:
                    return f"Error: executing Python file: {e}"
            else:
                return f'Error: "{file_path}" is not a Python file.'
        else:
            return f'Error: File "{file_path}" not found.'
    else:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'