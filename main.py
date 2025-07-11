import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    message = ""
    system_prompt = "I\'M JUST A ROBOT"
    if len(sys.argv) == 1:
        print("No message was provided")
        sys.exit(1)
    else:
        message = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=message)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    verbose = '--verbose' in sys.argv
    if verbose:
        print(f"User prompt: {message}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(system_prompt)

if __name__ == "__main__":
    main()


