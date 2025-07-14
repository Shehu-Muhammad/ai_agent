import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.get_write_file import schema_write_file, write_file

function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    else:
        # Step 1: fetch the function
        func = function_map[function_name]

        # Step 2: make a copy of the args and add the directory
        args = dict(function_call_part.args)
        args["working_directory"] = "./calculator"

        # Step 3: call it with keyword arguments
        function_result = func(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )

def main():
    verbose = '--verbose' in sys.argv
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    message = ""
    system_prompt = system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    if len(sys.argv) == 1:
        print("No message was provided")
        sys.exit(1)
    else:
        message = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=message)]),
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )

    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose = verbose)

            # Error check: Is the function response present?
            if not (
                hasattr(function_call_result.parts[0], "function_response")
                and hasattr(function_call_result.parts[0].function_response, "response")
            ):
                raise Exception("No function response found!")

            # Only print response if verbose
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    
    else:
        print(response.text)

    if verbose:
        print(f"User prompt: {message}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()


