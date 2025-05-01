import os
import streamlit as st
from streamlit.errors import StreamlitAPIException
import ast
import random
from attrs import define
from bedrock_integration import generate_text, BASE_PROMPT

st.title('Predictive Planner')


@define
class ModelResponse:
    text: str | None
    error: str | None

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        try:
            df_content = ast.literal_eval(message["content"])
            st.dataframe(df_content)
        except (SyntaxError, ValueError, StreamlitAPIException):
            st.write(message["content"])

if prompt:= st.chat_input('What do you want to know about the data?'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    raw_response = generate_text(BASE_PROMPT + prompt)
    response = ModelResponse(text=raw_response, error=None)
    if response.error:
        st.session_state.messages.append({'role': 'assistant', 'content': str(response.error)})
        with st.chat_message('assistant'):
            print('Invalid response received')
            print(response.error)
            st.write(response.error)
            st.write('Invalid response received. Probably a server error. Try again.')
    else:
        result = response.text
        st.session_state.messages.append({'role': 'assistant', 'content': str(result)})
        with st.chat_message('assistant'):
            st.write(result)
