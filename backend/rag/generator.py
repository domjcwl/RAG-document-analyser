def build_prompt(relevant_chunks, chat_history, user_query):
    context = "\n\n".join(relevant_chunks) #the top k chunks
    history = "\n".join(
        [f"{m['role']}: {m['content']}" for m in chat_history]
    )

    return f"""
You are a helpful assistant.
Respond to the user question based solely on the context chunks.
Use the chat history to aid you in your reply.

Chat history:
{history}

Context Chunks:
{context}

User question:
{user_query}
"""





#for context, your memory structure looks like this, one dictionary is one "m"
'''
[
  {"role": "user", "content": "What is TCP?"},
  {"role": "assistant", "content": "TCP is a transport protocol"}
]
'''
#hence the use of ( f"{m['role']}: {m['content']}" for m in chat_history )