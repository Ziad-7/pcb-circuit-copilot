import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PCB Component & Circuit Troubleshooting Assistant"
    API_V1_STR: str = ""
    
    # Embeddings & Vector Store
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VECTOR_STORE_PATH: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "vector_store")
    )
    COLLECTION_NAME: str = "pcb_datasheets"
    TOP_K_RESULTS: int = 2
    
    # LLM Settings
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "llama3.2:1b"
    LLM_TEMPERATURE: float = 0.1
    
    class Config:
        case_sensitive = True

settings = Settings()
