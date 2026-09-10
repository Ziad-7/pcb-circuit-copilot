from typing import List, Dict, Any, Optional
import ollama
from app.core.config import settings
from app.utils.logging_config import logger

class GenerationService:
    def __init__(self):
        self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)
        self.model = settings.OLLAMA_MODEL

    def check_health(self) -> bool:
        try:
            self.client.list()
            return True
        except Exception as e:
            logger.warning(f"Ollama health check failed: {e}")
            return False

    def build_prompt(self, question: str, contexts: List[Dict[str, Any]], visual_context: Optional[str] = None) -> str:
        evidence_blocks = []
        for c in contexts:
            evidence_blocks.append(f"[Datasheet: {c['source']} (Page {c['page']})]\n{c['text']}")
        joined_evidence = "\n\n".join(evidence_blocks)
        
        vision_section = ""
        if visual_context:
            vision_section = f"\n[Visual Component Detections]: {visual_context}\n"
            
        system_instructions = (
            "You are an expert electrical and electronics engineering assistant.\n"
            "Provide the step-by-step technical pinout, voltage limit, or diagnostic procedure using ONLY the manufacturer datasheet evidence below.\n"
            "Always include the document source citation (Datasheet name and Page number) at the end."
        )
        
        prompt = (
            f"System: {system_instructions}\n"
            f"{vision_section}\n"
            f"[MANUFACTURER DATASHEET EVIDENCE]:\n{joined_evidence}\n\n"
            f"User Question: {question}\n\n"
            f"Engineering Response:"
        )
        return prompt

    def generate(self, question: str, contexts: List[Dict[str, Any]], visual_context: Optional[str] = None) -> str:
        if not contexts:
            return "No relevant component datasheet records found for this circuit scenario."

        prompt = self.build_prompt(question, contexts, visual_context)
        top = contexts[0]
        fallback_answer = f"Technical Specification: {top['text']} [Source: {top['source']}, Page {top['page']}]"
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": settings.LLM_TEMPERATURE}
            )
            ans = response["message"]["content"].strip()
            if len(ans) < 15:
                return fallback_answer
            return ans
        except Exception as e:
            logger.warning(f"Ollama generation exception: {e}. Utilizing grounded fallback.")
            return fallback_answer

generation_service = GenerationService()
