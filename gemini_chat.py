import os
from google import genai
from google.genai import types
from dotenv import load_dotenv  # This is the new import you need

# Load environment variables from .env file
# This MUST happen before you try to access any environment variables
load_dotenv()

import os
from google import genai
from google.genai import types


def generate(entrada:str):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=entrada),
            ],
        ),
    ]
    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        response_mime_type="text/plain",
    )

    resposta=""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        resposta+=chunk.text
    return resposta

#if __name__ == "__main__":
#    # Test it to make sure it works
#    test_response = generate(entrada="Hello, how's the weather today in New York?")
#    print(f"Test response: {test_response}")