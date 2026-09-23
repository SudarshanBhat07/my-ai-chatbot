import streamlit as st
from google import genai


# Connect to Gemini
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


def get_ai_response(messages):

    # Only keep recent messages
    # This prevents the request becoming too large
    recent_messages = messages[-10:]

    conversation = ""

    for message in recent_messages:

        if message["role"] == "user":
            conversation += f"User: {message['content']}\n"

        elif message["role"] == "assistant":
            conversation += f"Assistant: {message['content']}\n"

    conversation += "Assistant:"

    try:

        # Stream the response
        response = client.models.generate_content_stream(
            model="gemini-3.6-flash",
            contents=conversation
        )

        for chunk in response:

            if chunk.text:
                yield chunk.text


    except Exception as e:

        error = str(e)

        if "503" in error or "UNAVAILABLE" in error:

            yield (
                "The AI service is temporarily busy. "
                "Please try again in a moment."
            )

        elif "429" in error:

            yield (
                "The API usage limit has been reached. "
                "Please try again later."
            )

        elif "404" in error:

            yield (
                "The selected AI model is currently unavailable."
            )

        else:

            yield f"Error: {error}"
