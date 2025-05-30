#set GROQ_API_KEY=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
import os
import chainlit as cl
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from groq import Groq

# Load API Key
groq_api_key = os.getenv("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")
groq_client = Groq(api_key=groq_api_key)

# Load dataset
df = pd.read_csv('RamayanDataSet.csv')
df.columns = df.columns.str.strip()  # Clean up any leading/trailing whitespace
verses = df['English Translation'].dropna().tolist()


# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")
verse_embeddings = embedder.encode(verses, convert_to_tensor=True)

# Fact-check function
def check_fact(statement):
    statement_embedding = embedder.encode(statement, convert_to_tensor=True)
    cos_scores = util.cos_sim(statement_embedding, verse_embeddings)[0]
    top_results = torch.topk(cos_scores, k=3)
    top_verses = [verses[i] for i in top_results[1]]

    prompt = f"""
You are a Ramayana expert. Based only on the following verses from the Valmiki Ramayana:

1. {top_verses[0]}
2. {top_verses[1]}
3. {top_verses[2]}

Determine if the user statement is factually correct. If yes, return "True", if factually wrong return "False". If irrelevant or vague, return "None".
User statement: "{statement}"
Answer:"""

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = response.choices[0].message.content.strip().lower()

    if "true" in answer:
        return "✅ True – That is correct based on the Ramayana."
    elif "false" in answer:
        return "❌ False – That is incorrect based on the Ramayana."
    else:
        return "🤔 None – The statement is vague or irrelevant to the Ramayana."

# Chainlit entrypoint
@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content.strip()
    reply = check_fact(user_input)
    await cl.Message(content=reply).send()
