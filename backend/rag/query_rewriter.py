import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client
# It looks for the environment variable "GROQ_API_KEY" by default
client = Groq(api_key=api_key)

def rewrite_query(chat_history: list, user_query: str) -> str:
    """
    Uses Groq to rewrite the user query into a 
    standalone, context-rich search query.
    """
    history = "\n".join(
        [f"{m['role']}: {m['content']}" for m in chat_history]
    )

    prompt = f"""
    
This is a application where I insert files/documents and the asks questions based on this file/document. 

You are a query rewriting assistant.

Given the conversation history and the user's latest question,
rewrite the question into a standalone, explicit query that
can be used for semantic search. If there is no conversation in the 
conversation history, don't change the user question.

Conversation history:
{history}

User question:
{user_query}

Rewritten standalone query:
"""

    # Use a Groq-supported model like llama-3.3-70b-versatile
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"system", "content":"do whatever, the user tells you to do"},{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()