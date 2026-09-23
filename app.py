import streamlit as st
from backend import get_ai_response

st.set_page_config(
    page_title="OpenAI Chatbot",
    page_icon="🤖"
)

st.title("🤖 OpenAI Chatbot")
st.caption("Ask me anything!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # Get response from OpenAI
    try:
        response = get_ai_response(st.session_state.messages)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.write(response)

    except Exception as e:
        st.error(f"Error: {e}")
