from fastapi import FastAPI, UploadFile, File,HTTPException
from app.schemas import ChatRequest
from chatmemory.chat_memory import ChatMemory
from vectorDB.init_store import build_vector_store_from_file
from rag.query_rewriter import rewrite_query
from rag.retriever import retrieve_with_rewritten_query
from rag.prompt_builder import build_prompt
from rag.llm import call_llm
import tempfile
import os
from fastapi.middleware.cors import CORSMiddleware



UPLOAD_DIR = "uploads"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



# -----------------------------
# Global state
# -----------------------------
database = None
memory = ChatMemory()


# -----------------------------
# Upload endpoint
# -----------------------------

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global database, memory

    # Reset chat memory for new document
    memory = ChatMemory()

    # Validate file type early
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF or TXT files are supported")

    # Create a temporary file
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        temp_path = tmp.name
        contents = await file.read()
        tmp.write(contents)

    try:
        # Build vector store from temp file
        database = build_vector_store_from_file(temp_path)
    finally:
        # Always remove temp file
        os.remove(temp_path)

    return {
        "status": "success",
        "filename": file.filename
    }

# -----------------------------
# Chat endpoint
# -----------------------------
@app.post("/chat")
def chat(req: ChatRequest):
    if database is None:
        return {"error": "No document uploaded yet"}

    # 1️⃣ Store user message
    memory.add_to_chat_history("user", req.message)

    # 2️⃣ Rewrite query
    rewritten_query = rewrite_query(
        chat_history=memory.get_from_chat_history(),
        user_query=req.message
    )

    # 3️⃣ Retrieve context
    context_chunks = retrieve_with_rewritten_query(
        rewritten_query,
        database
    )

    # 4️⃣ Build prompt
    prompt = build_prompt(
        relevant_chunks=context_chunks,
        chat_history=memory.get_from_chat_history(),
        user_query=req.message
    )

    # 5️⃣ LLM call
    answer = call_llm(prompt)

    # 6️⃣ Store assistant response
    memory.add_to_chat_history("assistant", answer)

    return {
        "answer": answer
    }
    
    
@app.post("/remove")
def remove_file():
    global database, memory

    database = None
    memory = ChatMemory()

    return {
        "status": "success",
        "message": "Document removed and chat memory reset"
    }

