import streamlit as st
from google import genai


# Create Gemini client
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


def get_ai_response(messages):

    # Build conversation history
    conversation = ""

    for message in messages:
        if message["role"] == "user":
            conversation += f"User: {message['content']}\n"

        elif message["role"] == "assistant":
            conversation += f"Assistant: {message['content']}\n"

    conversation += "Assistant: "

    try:
        # Streaming response
        response = client.models.generate_content_stream(
            model="gemini-3.8-flash",
            contents=conversation
        )

        # Send each piece of text to app.py
        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:

        error_message = str(e)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            yield (
                "Gemini is currently experiencing high demand. "
                "Please try again in a moment."
            )

        elif "429" in error_message:
            yield (
                "The Gemini API usage limit has been reached. "
                "Please try again later."
            )

        elif "404" in error_message:
            yield (
                "The selected Gemini model is unavailable. "
                "Please check the model name."
            )

        else:
            yield f"Something went wrong: {error_message}"
