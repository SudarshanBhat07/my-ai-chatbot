import streamlit as st
from google import genai

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

def get_ai_response(messages):
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
