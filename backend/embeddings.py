from sentence_transformers import SentenceTransformer
from loaders import load_document
from chunker import chunk_text


model = SentenceTransformer("all-MiniLM-L6-v2")

if __name__ == "__main__":
    file_path = input("File Path: ")
    file_path = file_path.strip().replace('"','')
    text = load_document(file_path)
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)  # embeds each chunk in the chunks list independently and returns a list of vectors.

    print("Number of chunks:", len(chunks))
    print("Embedding shape:", embeddings.shape)
