import os
from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.utils.logging_config import logger

class RetrievalService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RetrievalService, cls).__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self):
        logger.info(f"Initializing RetrievalService with model: {settings.EMBEDDING_MODEL}")
        self.embed_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        logger.info(f"Opening ChromaDB at: {settings.VECTOR_STORE_PATH}")
        self.chroma_client = chromadb.PersistentClient(path=settings.VECTOR_STORE_PATH)
        self.collection = self.chroma_client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"RetrievalService ready: {self.collection.count()} chunks indexed.")

    def get_chunk_count(self) -> int:
        return self.collection.count()

    def retrieve(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        k = top_k or settings.TOP_K_RESULTS
        q_vec = self.embed_model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=q_vec,
            n_results=min(k, max(1, self.collection.count()))
        )
        
        contexts = []
        if results and results.get("documents") and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0]
            for d, m, dist in zip(docs, metas, dists):
                contexts.append({
                    "text": d,
                    "source": m.get("source", "Unknown_Datasheet.pdf"),
                    "page": m.get("page", 1),
                    "score": round(1.0 - dist, 4)
                })
        return contexts

retrieval_service = RetrievalService()
