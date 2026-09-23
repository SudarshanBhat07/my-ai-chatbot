import streamlit as st
from backend import get_ai_response

# Page settings
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Chatbot")
st.caption("Ask me anything!")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
user_input = st.chat_input("Type your message...")


if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)


    # Generate AI response
    with st.chat_message("assistant"):

        try:
            response = st.write_stream(
                get_ai_response(st.session_state.messages)
            )

        except Exception:
            response = "Sorry, I couldn't generate a response. Please try again."
            st.error(response)


    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
