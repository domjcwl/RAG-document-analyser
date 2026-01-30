from loaders import load_pdf, load_txt
from chunker import chunk_text
from embedder import embed_texts
from vectorDB.faiss_db import FAISSStore

database = FAISSStore(dim=1536)

def ingest_file(path: str):
    if path.endswith(".pdf"):
        text = load_pdf(path)
    elif path.endswith("load.txt"):
        text = load_txt(path)
    else:
        print("Unsupported file type")
        return

    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    
    doc_id = path
    database.add(embeddings, chunks, doc_id)
