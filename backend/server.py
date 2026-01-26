from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from resume_loader import load_document
from chunker import chunk_text
from embeddings import model
from vector_store import create_index, add_embeddings, search
from llm import build_rag_prompt, generate_answer
import tempfile

app = FastAPI()

# Allow CORS so frontend can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "RAG backend is alive"}

@app.post("/ask")
async def ask(file: UploadFile, question: str = Form(...)): #run the following when a POST request is made to /ask with a file and question
    # Save file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    # 1️⃣ Load and chunk document
    text = load_document(file_path)
    chunks = chunk_text(text)

    # 2️⃣ Embed chunks
    chunk_embeddings = model.encode(chunks)

    # 3️⃣ Create FAISS index
    index = create_index(chunk_embeddings.shape[1])
    add_embeddings(index, np.array(chunk_embeddings))

    # 4️⃣ Embed question
    query_embedding = model.encode([question])

    # 5️⃣ Retrieve relevant chunks
    _, indices = search(index, query_embedding, top_k=2)
    relevant_chunks = [chunks[i] for i in indices[0]]

    # 6️⃣ Build prompt
    prompt = build_rag_prompt(relevant_chunks, question)

    # 7️⃣ Generate answer
    answer = generate_answer(prompt)

    return {"answer": answer}