from openai import OpenAI

client = OpenAI()

def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in response.data] # returns a list of vectors for for each chunk. [[floats1],[floats2],[floats3],[floats4],...]
