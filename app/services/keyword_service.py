from rank_bm25 import BM25Okapi
import numpy as np
from app.logs import Log

class KeywordSearch:

    def __init__(self, texts, metadata):
        self.texts = texts
        self.metadata = metadata
        self.tokenized_corpus = [text.lower().split() for text in texts]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        self.logger = Log.get("keyword_search")

    def search(self, query, k=20):
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        top_indices = np.argsort(scores)[::-1][:k]

        results = []

        for idx in top_indices:
            self.logger.info(
                            f"keyword_score: {float(scores[idx])} | "
                            f"index: {idx} | "
                            f"metadata: {self.metadata[idx]}")
            results.append({
                "text": self.texts[idx],
                "keyword_score": float(scores[idx]),
                "index": idx,
                "metadata": self.metadata[idx]
            })

        return results
