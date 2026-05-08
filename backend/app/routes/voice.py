from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai_service import get_ai_response

router = APIRouter()

class VoiceRequest(BaseModel):
    query: str

@router.post("/voice-query")
def voice_query(req: VoiceRequest):
    response = get_ai_response(req.query)

    return {
        "answer": response
    }