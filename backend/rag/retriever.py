from ingestion.embedder import embed_texts

def retrieve_with_rewritten_query(rewritten_query: str,vector_DB,top_k: int = 5):
    query_embedding = embed_texts([rewritten_query])[0]
    return vector_DB.search(query_embedding, top_k)
