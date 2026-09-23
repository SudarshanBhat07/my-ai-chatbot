import streamlit as st
from google import genai
import time

# Connect to Gemini
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

    # Try up to 3 times
    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=conversation
            )

            # Return Gemini answer
            if response.text:
                return response.text

            return "I couldn't generate a response. Please try again."

        except Exception as e:

            error_message = str(e)

            # Temporary server problem
            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < 2:
                    time.sleep(2)
                    continue

                return (
                    "Gemini is currently experiencing high demand. "
                    "Please try again in a moment."
                )

            # Rate limit / quota
            elif "429" in error_message:

                return (
                    "The Gemini API usage limit has been reached. "
                    "Please try again later."
                )

            # Other error
            else:
                return f"Unable to process your request: {error_message}"

    return "Unable to generate a response. Please try again."
