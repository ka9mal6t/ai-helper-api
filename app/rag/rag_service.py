from app.rag.document_loader import load_pdf, chunk_text
from app.rag.embedding_service import embed_texts, embed_query
from app.rag.vector_store import VectorStore
import os


class RAGService:

    def __init__(self, files):

        all_chunks = []
        self.metadata = []

        for filepath in files:

            text = load_pdf(filepath)
            chunks = chunk_text(text)

            for chunk in chunks:
                all_chunks.append(chunk)
                self.metadata.append({
                    "source": filepath
                })

        embeddings = embed_texts(all_chunks)

        self.store = VectorStore(len(embeddings[0]))
        self.store.add(embeddings, all_chunks)
        


    def retrieve(self, question):
        query_embedding = embed_query(question)
        return self.store.search(query_embedding)
