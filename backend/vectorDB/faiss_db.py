import faiss
import numpy as np

class FAISSStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)  #index is the database that stores all the embedded chunks (vectors) of a specific shape (dimension)
        self.chunks = []

    def add(self, embeddings, chunks):
        self.index.add(np.array(embeddings).astype("float32")) #adding the vectors to the database
        self.chunks.extend(chunks) #adds the chunks into the list for referencing later.

    def search(self, query_embedding, top_k=5): #give the top 5 vectors that are similar to the query embedding vector.
        Distance, Indices = self.index.search(
            np.array([query_embedding]).astype("float32"),
            top_k
        )
        return [self.chunks[i] for i in Indices[0]]
