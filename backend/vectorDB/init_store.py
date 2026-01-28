from ingestion.loaders import load_pdf, load_txt
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_texts
from .faiss_db import FAISSStore






def build_vector_store_from_file(file_path: str) -> FAISSStore:
    database = FAISSStore(dim=384)

    if file_path.endswith(".pdf"):
        text = load_pdf(file_path)
    elif file_path.endswith(".txt"):
        text = load_txt(file_path)
    else:
        raise ValueError("Unsupported file type")

    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    database.add(embeddings, chunks)

    return database