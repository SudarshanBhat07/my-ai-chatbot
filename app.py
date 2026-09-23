import streamlit as st
from backend import get_ai_response


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖"
)


# --------------------------------
# Title
# --------------------------------

st.title("🤖 Gemini AI Chatbot")

st.caption("Powered by Google Gemini")


# --------------------------------
# Create Chat History
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------
# Display Previous Messages
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------
# User Input
# --------------------------------

user_input = st.chat_input(
    "Type your message..."
)


# --------------------------------
# When User Sends Message
# --------------------------------

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)


    # --------------------------------
    # Generate Gemini Response
    # --------------------------------

    with st.chat_message("assistant"):

        try:

            # Stream Gemini response
            response = st.write_stream(
                get_ai_response(
                    st.session_state.messages
                )
            )

        except Exception as e:

            response = (
                "Sorry, something went wrong. "
                "Please try again."
            )

            st.error(response)


    # --------------------------------
    # Save Gemini Response
    # --------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
