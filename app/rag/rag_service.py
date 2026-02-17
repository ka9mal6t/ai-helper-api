from app.rag.document_loader import load_pdf, chunk_text
from app.rag.embedding_service import embed_texts, embed_query
from app.rag.vector_store import VectorStore
import os


class RAGService:

    def __init__(self, path, files):
       
        index_exists = os.path.exists(os.path.join(path, "vector_index/faiss.index"))

        if index_exists:
            print("Loading existing FAISS index...")
            self.store = VectorStore(path)
            return

        print("Building new FAISS index...")

        all_chunks = []
        metadata = []

        for file in files:
            print(file)
            text = load_pdf(file)
            chunks = chunk_text(text)

            for chunk in chunks:
                all_chunks.append(chunk)
                metadata.append({
                    "source": file.split('\\')[-1]
                })


        embeddings = embed_texts(all_chunks)

        self.store = VectorStore(path, len(embeddings[0]))
        self.store.add(embeddings, all_chunks, metadata)

        self.store.save()
        


    def retrieve(self, question):
        query_embedding = embed_query(question)
        return self.store.search(query_embedding)
