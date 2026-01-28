
from fastapi import FastAPI
from app.schemas import ChatRequest
from chatmemory.chat_memory import ChatMemory
from vectorDB.init_store import build_vector_store_from_file
from rag.query_rewriter import rewrite_query
from rag.retriever import retrieve_with_rewritten_query
from rag.prompt_builder import build_prompt
from rag.llm import call_llm

app = FastAPI()

# 🔹 Build vector store ONCE at startup
database = build_vector_store_from_file(r"C:\Users\booong\Downloads\Resume.pdf")

# 🔹 Initialize chat memory
memory = ChatMemory()

@app.post("/chat")
def chat(req: ChatRequest):
    # 1️⃣ Store original user message
    memory.add_to_chat_history("user", req.message)

    # 2️⃣ Rewrite query using history
    rewritten_query = rewrite_query(
        chat_history=memory.get_from_chat_history(),
        user_query=req.message
    )


    # 3️⃣ Retrieve context
    context_chunks = retrieve_with_rewritten_query(rewritten_query,database)

    # 4️⃣ Build prompt using ORIGINAL query
    prompt = build_prompt(
        relevant_chunks=context_chunks,
        chat_history=memory.get_from_chat_history(),
        user_query=req.message
    )


    # 5️⃣ Generate answer
    answer = call_llm(prompt)

    # 6️⃣ Store assistant response
    memory.add_to_chat_history("assistant", answer)

    return {
        "answer": answer,
        "rewritten_query": rewritten_query
    }
