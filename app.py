"""
This script is inspired by marshmellow77. 
Checkout the github repo: https://github.com/marshmellow77/streamlit-chatgpt-ui/tree/main
"""

import os
import re
import json

from dotenv import load_dotenv
import openai
import streamlit as st
from streamlit_chat import message

# Load environment variables from .env file
load_dotenv()

# openai key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# List of OpenAI models
GPT_3_5 = "GPT-3.5"
GPT_4 = "GPT-4"


class chatUI:

    def __init__(self) -> None:

        self.initialize_session_state()

        self.sidebar_ui()

        # define json object to save the chat history
        self.chat_history = []

        # container for chat history
        self.response_container = st.container()
        # container for text box
        self.container = st.container()

        self.model_selection()

        # Reset chat
        if self.clear_button:
            self.reset_chat_session()

        self.create_chat_ui()

        # Save chat history
        if st.sidebar.button("Save"):
            self.save_to_file()

    # Initialize session state variables
    def initialize_session_state(self) -> None:
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []
        if 'messages' not in st.session_state:
            st.session_state['messages'] = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
        if 'model_name' not in st.session_state:
            st.session_state['model_name'] = []

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
        self.file_path = st.sidebar.text_input(
            "File path", "", help="Enter the file path to save the chat history.")
        self.chat_name = st.sidebar.text_input(
            "Chat name", "", help="Enter the name of the file.")

    def model_selection(self) -> None:

        # Map model names to OpenAI model IDs
        if self.model_name == GPT_3_5:
            self.model = "gpt-3.5-turbo"
        else:
            self.model = "gpt-4"

    # reset the chat session
    def reset_chat_session(self) -> None:

        st.session_state['generated'] = []
        st.session_state['past'] = []
        st.session_state['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # Call GPT
    def generate_response(self, prompt) -> str:

        st.session_state['messages'].append(
            {"role": "user", "content": prompt})

        msgs = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        msgs += st.session_state['messages'][-9:]

        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=st.session_state['messages'],
            temperature=self.model_temp
        )
        response = completion.choices[0].message.content
        st.session_state['messages'].append(
            {"role": "assistant", "content": response})

        # print(st.session_state['messages'])

        return response

    def save_to_file(self) -> None:

        combined_path = os.path.join(self.file_path, self.chat_name+'.json')

        # save the chat history to the user-defined directory
        with open(combined_path, "w") as json_file:
            json.dump(self.chat_history, json_file)

        st.success("Chat history saved!")

    def create_chat_ui(self, chat_container_key='new_form', user_input_key='new_input') -> None:

        with self.container:
            with st.form(key=chat_container_key, clear_on_submit=True):
                user_input = st.text_area(
                    "You:", key=user_input_key, height=100)
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = self.generate_response(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        if st.session_state['generated']:
            with self.response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i],
                            is_user=True, key=str(i) + '_user')
                    st.header(f":robot_face: \n")
                    st.markdown(st.session_state["generated"][i])
                    self.chat_history.append({'user': st.session_state["past"][i],
                                              'system': st.session_state["generated"][i]
                                              }
                                             )


if __name__ == "__main__":

    chat_ui = chatUI()
