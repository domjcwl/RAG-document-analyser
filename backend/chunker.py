from loaders import load_document


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap  # move back for overlap

    return chunks




if __name__ == "__main__":
    file_path = input("File Path: ")
    file_path = file_path.strip().replace('"','')
    text = load_document(file_path)
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---")
        print(chunk)