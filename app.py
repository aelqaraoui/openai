import os
import json
import openai
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from openai.embeddings_utils import cosine_similarity

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

if 'text' not in st.session_state:
    f = open("text.data", "r")
    st.session_state['text'] = f.read().split("\n")

if 'embeddings' not in st.session_state:
    f = open("embeddings.txt", "r")
    st.session_state['embeddings'] = [json.loads(embedding) for embedding in f.read().split("\n")[1:]]

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = ""

with st.form("my_form", clear_on_submit=True):
    question = st.text_input('Prompt', '')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted and (len(question.replace(" ", "")) > 0):

        question_embedding = get_embedding(question)
        similarities = [cosine_similarity(i, question_embedding) for i in st.session_state['embeddings']]
        context = st.session_state['text'][np.array(similarities).argmin()]
            
        prompt = context + st.session_state['conversation'] + "\n\n" + "Q: " + question + "\nA:"

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
        
        st.session_state['conversation'] = st.session_state['conversation'] + "\n\n" + "Q: " + question + "\nA:" + answer



components.html(f'<p  style="white-space: pre-line;word-wrap:break-word;color:white;">{st.session_state["conversation"]}</p>', height=900, scrolling=True)
