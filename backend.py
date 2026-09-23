import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def get_ai_response(messages):

    # Convert chat history into simple text
    conversation = ""

    for message in messages:
        if message["role"] == "user":
            conversation += f"User: {message['content']}\n"
        else:
            conversation += f"Assistant: {message['content']}\n"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation
    )

    return response.text