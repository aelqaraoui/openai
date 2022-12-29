import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

from openai.embeddings_utils import cosine_similarity

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

f = open("text.data", "r")

text = f.read().split("\n")

f = open("embeddings.txt", "r")

embeddings = f.read().split("\n")[1:]
embeddings = json.loads(embeddings[0])

question = "Whos is osho"
question_embedding = get_embedding(question)


similarities = [cosine_similarity(i, question_embedding) for i in embeddings]

import numpy as np

context = text[np.array(similarities).argmax()]