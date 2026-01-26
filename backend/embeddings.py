from sentence_transformers import SentenceTransformer
from resume_loader import load_document
from chunker import chunk_text


model = SentenceTransformer("all-MiniLM-L6-v2")
# this model gives a dimesion = 384 for each chunk. e.g. (1 row, 384 columns) for one chunk
# 5 chunks equal (5 rows, 384 columns)

if __name__ == "__main__":
    file_path = input("File Path: ")
    file_path = file_path.strip().replace('"','')
    text = load_document(file_path)
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)  # embeds each chunk in the chunks list independently and returns a LIST OF VECTORS.

    print("Number of chunks:", len(chunks))
    print("Embedding shape:", embeddings.shape)

