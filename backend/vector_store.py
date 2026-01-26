import faiss
import numpy as np


# A FAISS index is a data structure used to store and efficiently search through large sets of high-dimensional vectors. You are creating an index which stores vectors of dimension 384
def create_index(embedding_dimension: int):
    index = faiss.IndexFlatL2(embedding_dimension)
    return index

# the created index and the numpy array (lists) of embeddings are set as arguments.
def add_embeddings(index, embeddings: np.ndarray):
    index.add(embeddings)
    

def search(index, query_embedding: np.ndarray, top_k: int = 3):  #query_embedding must be shaped like (1,embedding_dim) and wrapped in a list    #top_k, where k is the top vectors that match
    distances, indices = index.search(query_embedding, top_k) #distances and indices are 2d arrays. e.g. distances = [[0.12, 0.34]]   indices   = [[2, 0]] closest vector:index2 | second closest vector:index0
    return distances, indices