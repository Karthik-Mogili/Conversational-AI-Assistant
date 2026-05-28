import streamlit as st
from chatbot_engine import ChatbotEngine

# Page Configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize Chatbot
if "chatbot" not in st.session_state:

    st.session_state.chatbot = ChatbotEngine()

# Sidebar Settings
with st.sidebar:

    st.title("⚙️ Settings")

    # Model Selection
    model_choice = st.selectbox(
        "Select Model",
        [
            "llama-3.3-70b-versatile",
            "llama3-8b-8192"
        ],
        index=0
    )

    # Update model
    st.session_state.chatbot.model = model_choice

    # Chain of Thought option
    use_cot = st.checkbox(
        "Use Chain-of-Thought",
        value=False
    )

    # Clear history button
    if st.button("Clear Chat History"):

        st.session_state.chatbot.clear_history()

        st.rerun()

# Main Title
st.title("🤖 AI Chatbot")

# Display Chat History
for message in st.session_state.chatbot.get_history():

    # Skip system messages
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Function to generate response
def process_response(user_input):

    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        try:

            # Generate streaming response
            response = st.session_state.chatbot.chat(
                user_input,
                use_cot=use_cot,
                stream=True
            )

            for chunk in response:

                if chunk.choices[0].delta.content is not None:

                    full_response += chunk.choices[0].delta.content

                    message_placeholder.markdown(
                        full_response + "▌"
                    )

            # Final response
            message_placeholder.markdown(full_response)

            # Save assistant response
            st.session_state.chatbot.append_assistant_response(
                full_response
            )

        except Exception as e:

            st.error(f"Chat Error: {str(e)}")

# Chat Input
if prompt := st.chat_input("Type your message here..."):

    # Show user message
    st.chat_message("user").markdown(prompt)

    # Generate response
    process_response(prompt)