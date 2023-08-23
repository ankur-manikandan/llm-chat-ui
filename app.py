"""
This script is inspired by Streamlit's "Build conversational apps" tutorial.
Checkout the tutorial: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
"""

import os

from dotenv import load_dotenv
import openai
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# openai key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# List of OpenAI models
GPT_3_5 = "GPT-3.5"
GPT_4 = "GPT-4"


class chatUI:
    def __init__(self) -> None:

        self.initialize_session()

        self.sidebar_ui()

        self.model_selection()

        # Reset chat
        if self.clear_button:
            self.reset_chat_session()

        self.display_chat_history()

        self.create_chat_ui()

    def initialize_session(self) -> None:

        # initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def sidebar_ui(self) -> None:

        # define a sidebar
        st.sidebar.title("Chatbot")
        self.model_name = st.sidebar.radio(
            "Choose a GPT model:", (GPT_3_5, GPT_4))
        # Add a slider to the sidebar
        self.model_temp = st.sidebar.slider("Temperature", 0., 2., 1., 0.1)
        # Add a divider to the sidebar
        st.sidebar.markdown("---")
        self.clear_button = st.sidebar.button(
            "Clear Conversation", key="clear")

    def model_selection(self) -> None:

        # Map model names to OpenAI model IDs
        if self.model_name == GPT_3_5:
            self.model = "gpt-3.5-turbo"
        else:
            self.model = "gpt-4"

    # reset the chat session
    def reset_chat_session(self) -> None:

        st.session_state.messages = []

    def display_chat_history(self) -> None:

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def create_chat_ui(self) -> None:

        # user prompt
        if prompt := st.chat_input("Enter prompt"):
            # Add user message to chat history
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": m["role"], "content": m["content"]}
                              for m in st.session_state.messages],
                    stream=True,
                    temperature=self.model_temp
                ):
                    full_response += response.choices[0].delta.get(
                        "content", "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response})


if __name__ == '__main__':

    chatui = chatUI()
