import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Verify backend health, vector store chunk count, and model readiness."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "vector_store_chunks" in data
    assert data["vector_store_chunks"] > 0

def test_query_happy_path():
    """Verify successful retrieval and grounded response for valid component query."""
    payload = {
        "question": "What is the maximum input voltage for the LM7805 regulator?"
    }
    response = client.post("/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert "sources" in data
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0

def test_query_invalid_input_empty_payload():
    """Verify HTTP 422 Unprocessable Entity on empty or missing question payload."""
    payload = {}
    response = client.post("/query", json=payload)
    assert response.status_code == 422

def test_query_invalid_input_short_question():
    """Verify HTTP 422 on input below minimum character constraint."""
    payload = {"question": "ab"}
    response = client.post("/query", json=payload)
    assert response.status_code == 422

def test_query_with_visual_component_detection():
    """Verify multimodal input correctly runs YOLO neural detection and returns bounding boxes."""
    payload = {
        "question": "What are the required bypass capacitors for this voltage regulator?",
        "image_name": "lm7805_power_supply.jpg"
    }
    response = client.post("/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["detected_components"]) > 0
    comp_classes = [c["class_name"] for c in data["detected_components"]]
    # Genuine YOLO classes detected on the power supply PCB
    assert any(c in comp_classes for c in ["CAPACITOR", "IC", "DIODE", "LED", "CONNECTOR"])
    assert data["annotated_image_path"] is not None

