from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_texts(texts):
    """
    Создаёт embeddings для всех текстов с нормализацией.
    """
    texts = ["passage: " + t for t in texts]
    embeddings = model.encode(texts, normalize_embeddings=True)
    return np.array(embeddings, dtype="float32")


def embed_query(query):
    """
    Создаёт embedding для запроса.
    """
    query = "query: " + query
    embedding = model.encode([query], normalize_embeddings=True)
    return np.array(embedding[0], dtype="float32")
