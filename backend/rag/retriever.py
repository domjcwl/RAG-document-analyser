from ingestion.embedder import embed_texts

def retrieve(query: str, database, top_k=5):
    query_embedding = embed_texts([query])[0] #index 0 to retrieve the query vector. (REMEMBER, embed_text returns a list of vectors.)
    return database.search(query_embedding, top_k) #retrieve the top 5 most relevant vectors to the vector query
