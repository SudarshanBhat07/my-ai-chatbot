import streamlit as st
from openai import OpenAI

# -------------------------------
# PAGE SETTINGS
# -------------------------------

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 My AI Chatbot")
st.caption("Powered by OpenAI")


# -------------------------------
# OPENAI CONNECTION
# -------------------------------

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# -------------------------------
# CHAT HISTORY
# -------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# -------------------------------
# USER INPUT
# -------------------------------

prompt = st.chat_input("Type your message...")


# -------------------------------
# SEND TO OPENAI
# -------------------------------

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    try:

        # Send conversation to OpenAI
        response = client.responses.create(
            model="gpt-5.6",
            input=st.session_state.messages
        )

        # Get AI answer
        answer = response.output_text

        # Save AI answer
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Display AI answer
        with st.chat_message("assistant"):
            st.write(answer)

    except Exception as e:
        st.error(f"Error: {e}")
