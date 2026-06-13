"""
core/knowledge_base.py
-----------------------
Manages the ChromaDB vector store used by the Chat Agent (RAG).
Documents are chunked, embedded, and stored here after extraction.
"""
import uuid
import chromadb
from chromadb.utils import embedding_functions
from config.settings import CHROMA_DB_PATH, EMBEDDING_MODEL


class KnowledgeBase:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
        self.collection = self.client.get_or_create_collection(
            name="enterprise_docs",
            embedding_function=self.ef,
        )

    def add_document(self, text: str, metadata: dict | None = None) -> int:
        """Chunk text and insert into the vector store. Returns chunk count."""
        chunks = self._chunk_text(text)
        if not chunks:
            return 0
        ids = [str(uuid.uuid4()) for _ in chunks]
        metas = [metadata or {} for _ in chunks]
        self.collection.add(documents=chunks, ids=ids, metadatas=metas)
        return len(chunks)

    def query(self, question: str, n_results: int = 5) -> list[str]:
        """Return the top-n most relevant chunks for a question."""
        results = self.collection.query(
            query_texts=[question],
            n_results=min(n_results, self.collection.count() or 1),
        )
        return results["documents"][0] if results["documents"] else []

    def clear(self):
        """Delete and recreate the collection (wipes all docs)."""
        self.client.delete_collection("enterprise_docs")
        self.collection = self.client.get_or_create_collection(
            name="enterprise_docs",
            embedding_function=self.ef,
        )

    def count(self) -> int:
        return self.collection.count()

    # ------------------------------------------------------------------ #
    @staticmethod
    def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
        words = text.split()
        chunks, i = [], 0
        while i < len(words):
            chunk = " ".join(words[i : i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
            i += chunk_size - overlap
        return chunks
