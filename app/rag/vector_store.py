import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []
        self.metadata = []

    def add(self, embeddings, texts, metadata):
        self.index.add(np.array(embeddings))
        self.texts.extend(texts)
        self.metadata.extend(metadata)

    def search(self, query_embedding, k=5):
        D, I = self.index.search(
            np.array([query_embedding]).astype("float32"), k
        )

        results = []

        for idx in I[0]:
            results.append({
                "text": self.texts[idx],
                "metadata": self.metadata[idx]
            })

        return results
