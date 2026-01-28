from sentence_transformers import SentenceTransformer

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)
    return embeddings.tolist() # returns a list of vectors for for each chunk. [[floats1],[floats2],[floats3],[floats4],...] of dimension 384
