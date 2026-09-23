import streamlit as st
from google import genai
import time

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


def get_ai_response(messages):

    # Build conversation
    conversation = ""

    for message in messages:
        if message["role"] == "user":
            conversation += f"User: {message['content']}\n"
        else:
            conversation += f"Assistant: {message['content']}\n"

    # Find models available to this API key
    available_models = []

    try:
        for model in client.models.list():
            if "generateContent" in model.supported_actions:
                name = model.name.replace("models/", "")

                # Only use Gemini text models
                if "gemini" in name.lower():
                    available_models.append(name)

    except Exception:
        available_models = ["gemini-3.6-flash"]

    # Prefer Flash models
    flash_models = [
        model for model in available_models
        if "flash" in model.lower()
    ]

    # Try Flash models first
    models_to_try = flash_models + [
        model for model in available_models
        if model not in flash_models
    ]

    # Try available models
    for model_name in models_to_try[:5]:

        for attempt in range(2):

            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=conversation
                )

                if response.text:
                    return response.text

            except Exception as e:

                error = str(e)

                # Model busy - retry
                if "503" in error or "UNAVAILABLE" in error:

                    time.sleep(2)
                    continue

                # Model doesn't exist - try next model
                elif "404" in error:
                    break

                # Rate limit
                elif "429" in error:
                    return (
                        "The Gemini API usage limit has been reached. "
                        "Please try again later."
                    )

                else:
                    break

    return (
        "The AI service is temporarily unavailable. "
        "Please try again in a moment."
    )
