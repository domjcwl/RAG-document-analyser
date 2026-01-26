import os 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def build_rag_prompt(context_chunks, question): #context_chunks are the retrieved relevant chunks
    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful resume analyst.
Answer the question using ONLY the context below.
Answer in a concise and clear manner.
Answer based on sections of this exact resume.



Context:
{context_text}

Question:
{question}
"""
    return prompt


def generate_answer(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.25
    )

    return response.choices[0].message.content
