from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes.query import router as query_router
from app.services.retrieval import retrieval_service
from app.utils.logging_config import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-warming ChromaDB and embedding model in memory
    logger.info("Lifespan Startup: Pre-warming ChromaDB and embedding models...")
    count = retrieval_service.get_chunk_count()
    logger.info(f"Lifespan Startup Complete: {count} datasheet chunks ready for instant retrieval.")
    yield
    logger.info("Lifespan Shutdown: Cleaning up background resources.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Multimodal PCB Component & Circuit Troubleshooting Assistant (YOLO + RAG + FastAPI + Streamlit)",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(query_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
