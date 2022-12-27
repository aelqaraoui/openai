import os
import openai
import streamlit as st
import streamlit.components.v1 as components

openai.api_key = os.getenv("OPENAI_API_KEY")

if 'context' not in st.session_state:
    st.session_state['context'] = "Osho, also known as Bhagwan Shree Rajneesh, was an Indian spiritual leader and guru who founded the Rajneesh movement. He is known for his controversial teachings, which blended elements of Hinduism, Buddhism, and other Eastern and Western philosophies, and for his unconventional lifestyle and behavior. Osho's teachings focused on the idea of meditation and self-realization as a way to overcome the limitations of the ego and achieve a state of inner peace and enlightenment. He wrote more than 600 books on a wide range of subjects, including spirituality, psychology, and social issues. Despite his controversial reputation, Osho was widely respected and influential, and his teachings continue to be followed by many people around the world."
if 'context_length' not in st.session_state:
    st.session_state['context_length'] = len(st.session_state['context'])
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = ""

with st.form("my_form", clear_on_submit=True):
    question = st.text_input('Prompt', '')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        prompt = st.session_state['context'] + "\n\n" + "Q: " + question + "\nA:"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        
        answer = response.choices[0].text
        
        st.session_state['context'] = st.session_state['context'] + "\n\n" + "Q: " + question + "\nA:" + answer



components.html(f'<p  style="white-space: pre-line;word-wrap:break-word;color:white;">{st.session_state["context"][st.session_state["context_length"]:]}</p>', crolling=True)
