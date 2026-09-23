import streamlit as st
from backend import get_ai_response

st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 Gemini AI Chatbot")
st.caption("Ask me anything!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input box
user_input = st.chat_input("Type your message...")

if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # Send message to Gemini backend
    response = get_ai_response(
        st.session_state.messages
    )

    # Add Gemini response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)