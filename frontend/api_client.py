import os
import httpx
from typing import Dict, Any, Optional

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

class ApiClient:
    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url.rstrip("/")

    def check_health(self) -> Dict[str, Any]:
        try:
            with httpx.Client(timeout=4.0) as client:
                res = client.get(f"{self.base_url}/health")
                if res.status_code == 200:
                    return res.json()
        except Exception:
            pass
        return {"status": "offline", "vector_store_chunks": 0, "ollama_status": "disconnected"}

    def query(self, question: str, image_name: Optional[str] = None) -> Dict[str, Any]:
        payload = {"question": question, "image_name": image_name}
        with httpx.Client(timeout=60.0) as client:
            res = client.post(f"{self.base_url}/query", json=payload)
            res.raise_for_status()
            return res.json()

api_client = ApiClient()
