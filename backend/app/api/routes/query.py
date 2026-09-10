from fastapi import APIRouter, HTTPException
from app.schemas.query import QueryRequest, QueryResponse, HealthResponse, ComponentDetection
from app.services.retrieval import retrieval_service
from app.services.generation import generation_service
from app.services.vision import detect_pcb_components
from app.core.config import settings
from app.utils.logging_config import logger

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def get_health():
    chunk_count = retrieval_service.get_chunk_count()
    ollama_ok = generation_service.check_health()
    return HealthResponse(
        status="healthy" if chunk_count > 0 else "degraded",
        vector_store_chunks=chunk_count,
        ollama_status="connected" if ollama_ok else "disconnected",
        active_model=settings.OLLAMA_MODEL
    )

@router.post("/query", response_model=QueryResponse)
def handle_query(payload: QueryRequest):
    logger.info(f"Received circuit query: '{payload.question}' | Image: {payload.image_name}")
    
    # 1. Vision component detection
    visual_context, detected_items, annotated_path = detect_pcb_components(payload.image_name)
    
    # 2. Enrich query with detected component names (if specific)
    search_query = payload.question
    if detected_items:
        specific_comps = [d["class_name"] for d in detected_items[:2] if not d["class_name"].startswith("Electronic_Component_")]
        if specific_comps:
            search_query = f"{' '.join(specific_comps)} {payload.question}"
        
    # 3. Vector retrieval
    contexts = retrieval_service.retrieve(search_query)
    if not contexts:
        raise HTTPException(status_code=404, detail="No relevant datasheet specifications found.")
        
    # 4. LLM response generation
    answer = generation_service.generate(payload.question, contexts, visual_context)
    sources = [f"{c['source']} (Page {c['page']})" for c in contexts]
    
    detection_models = [
        ComponentDetection(
            class_name=d["class_name"],
            confidence=d["confidence"],
            box=d["box"],
            description=d["description"]
        )
        for d in detected_items
    ]
    
    return QueryResponse(
        answer=answer,
        sources=sources,
        detected_components=detection_models,
        visual_context=visual_context,
        annotated_image_path=annotated_path
    )
