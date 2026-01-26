import numpy as np
from resume_loader import load_document
from chunker import chunk_text
from embeddings import model
from vector_store import create_index, add_embeddings, search
from llm import build_rag_prompt, generate_answer

# 1️⃣ Load and chunk document
file_path = input("File Path: ")
file_path = file_path.strip().replace('"','')
text = load_document(file_path) # Load document from the given file path into text as a string dtype
chunks = chunk_text(text) # chunks is a list of text chunks

# 2️⃣ Embed chunks
chunk_embeddings = model.encode(chunks) # chunk_embeddings is a 2D array where each row is the embedding of the corresponding chunk

# 3️⃣ Create FAISS index
index = create_index(chunk_embeddings.shape[1])
add_embeddings(index, np.array(chunk_embeddings)) # Add the chunk embeddings to the FAISS index, argument only accepts np.arrays

# 4️⃣ User question
question = "run me through this resume document in detail."  # Example question

# 5️⃣ Embed question
query_embedding = model.encode([question]) # embed the query to compare with vectors in the vector database

# 6️⃣ Retrieve relevant chunks
_, indices = search(index, query_embedding, top_k=2) # Get the indices of the top 2 most relevant chunks, based on the query embedding, store them in indices
relevant_chunks = [chunks[i] for i in indices[0]]



# 7️⃣ Build prompt
prompt = build_rag_prompt(relevant_chunks, question)

# 8️⃣ Generate answer
answer = generate_answer(prompt)

print("\n=== ANSWER ===")
print(answer)
