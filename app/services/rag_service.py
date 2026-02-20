from app.services.document_loader import load_pdf, chunk_text
from app.services.embedding_service import embed_texts, embed_query
from app.services.vector_store import VectorStore
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
        

    def retrieve(self, question, max_chunks=8):
        query_embedding = embed_query(question)
        return self.store.search(query_embedding, max_chunks=max_chunks)
