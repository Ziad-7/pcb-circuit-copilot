from pydantic import BaseModel, Field
from typing import List, Optional

class ComponentDetection(BaseModel):
    class_name: str
    confidence: float
    box: List[int]
    description: str

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, description="Electronic circuit or component question")
    image_name: Optional[str] = Field(None, description="Filename of PCB image in data/images/ or uploaded")

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    detected_components: List[ComponentDetection]
    visual_context: Optional[str] = None
    annotated_image_path: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    vector_store_chunks: int
    ollama_status: str
    active_model: str
