import sqlite3
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
import re
import pickle
from transformers import GPT2TokenizerFast

print(openai.Model.list())

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

def importdb(db):
    f = open("text.data", "a")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    data=cursor.execute('''SELECT * FROM BOOKS''')
    
    max_ = 0

    for i, text in enumerate(data):
        f.write("\n" + re.sub(r'[^\x00-\x7F]+',' ', text[-1]).strip().replace("\n", " ").replace(";", " "))

    
#importdb("osho_books_002.db")

f = open("text.data", "r")

text = f.read().split("\n")

f = open("embeddings.txt", "a")

import json

for i, j in enumerate(text):
    l = get_embedding(j)
    print(f"{i+1} / {len(text)}")
    f.write("\n" + json.dumps(l))