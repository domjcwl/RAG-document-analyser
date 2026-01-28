from groq import Groq
import os
from dotenv import load_dotenv
from openai import api_key



def call_llm(prompt: str) -> str:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY_2")
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    response = call_llm("hey, hows your day")
    print(response)