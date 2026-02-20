from app.services.document_loader import load_pdf, chunk_text
from app.services.embedding_service import embed_texts, embed_query
from app.services.rerank_service import rerank
from app.services.vector_store import VectorStore
from app.services.keyword_service import KeywordSearch
import os
from app.logs import Log


class RAGService:

    def __init__(self, path, files):
        self.logger = Log.get("pdf")
        index_exists = os.path.exists(os.path.join(path, os.path.join(
            "vector_index", "faiss.index")))

        if index_exists:
            self.logger.info("Loading existing FAISS index...")
            self.store = VectorStore(path)
            self.keyword_search = KeywordSearch(self.store.texts, self.store.metadata)
            return

        self.logger.info("Building new FAISS index...")

        all_chunks = []
        metadata = []

        for file in files:
            self.logger.info(f"Processing {file}")
            text = load_pdf(file)
            chunks = chunk_text(text)
            for chunk in chunks:
                all_chunks.append(chunk)
                metadata.append({
                    "source": os.path.basename(file)
                })


        embeddings = embed_texts(all_chunks)

        self.store = VectorStore(path, len(embeddings[0]))
        self.store.add(embeddings, all_chunks, metadata)
        self.store.save()
        self.keyword_search = KeywordSearch(self.store.texts)
        

    def retrieve(self, question, n=8):
        query_embedding = embed_query(question)
        # 1️⃣ Embedding search   
        embedding_results = self.store.search(query_embedding)

        # 2️⃣ Keyword search
        keyword_results = self.keyword_search.search(question, k=15)

        
        # 3️⃣ Combine indexes
        combined_indices = set()
        for item in embedding_results:
            combined_indices.add(self.store.texts.index(item["text"]))

        for item in keyword_results:
            combined_indices.add(item["index"])
        
         # 4️⃣ Final chunks
        combined_chunks = []

        for idx in combined_indices:
            combined_chunks.append({
                "text": self.store.texts[idx],
                "metadata": self.store.metadata[idx]
            })

        reranked = rerank(question, combined_chunks, top_n=n)
        return reranked