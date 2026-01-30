import faiss
import numpy as np

class FAISSStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)  #index is the database that stores all the embedded chunks (vectors) of a specific shape (dimension)
        self.chunks = []
        self.doc_ids=[]

    def add(self, embeddings, chunks, doc_ids):
        self.index.add(np.array(embeddings).astype("float32")) #adding the vectors to the database
        self.chunks.extend(chunks) #adds the chunks into the list for referencing later.
        self.doc_ids.extend([doc_ids]*len(chunks)) #adds the document ids into the list for referencing later.
        
    def search(self, query_embedding, top_k=5): #give the top 5 vectors that are similar to the query embedding vector.
        Distance, Indices = self.index.search(
            np.array([query_embedding]).astype("float32"),
            top_k
        )
        return [self.chunks[i] for i in Indices[0]]
    
    def remove_document(self, doc_id):
        keep_indices = [i for i, d in enumerate(self.doc_ids) if d != doc_id]
        
        new_index = faiss.IndexFlatL2(self.index.d)
        new_texts = []
        new_docs_id=[]
        
        for i in keep_indices:
            vec = self.index.reconstruct(i)
            new_index.add(np.array([vec]).astype("float32"))
            new_texts.append(self.chunks[i])
            new_docs_id.append(self.doc_ids[i])

        self.index = new_index
        self.chunks = new_texts
        self.doc_ids = new_docs_id