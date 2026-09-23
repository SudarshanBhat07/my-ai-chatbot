import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

def get_ai_response(messages):

    response = client.responses.create(
        model="gpt-5.6",
        input=messages
    )

    return response.output_text
