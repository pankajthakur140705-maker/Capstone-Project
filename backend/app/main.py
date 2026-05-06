from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.routes import schemes, ai
from app.services.scheme_service import search_schemes
from app.services.ai_service import chat_with_ai   # ✅ FIXED (moved import properly)

# ----------------------------
# APP INIT
# ----------------------------
app = FastAPI(
    title="Bandhu AI",
    description="AI-powered government scheme recommendation system",
    version="2.0.0"
)

# ----------------------------
# CORS (React FRONTEND CONNECT FIX)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# ROUTERS
# ----------------------------
app.include_router(schemes.router)
app.include_router(ai.router)

# ----------------------------
# REQUEST MODELS
# ----------------------------
class SearchRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = {}

class ChatRequest(BaseModel):
    user_id: Optional[str] = "default"
    message: str

# ----------------------------
# ROOT TEST
# ----------------------------
@app.get("/")
def home():
    return {
        "message": "Bandhu AI Backend Running 🚀"
    }

# ----------------------------
# HEALTH CHECK (FRONTEND DEBUG)
# ----------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "backend": "running"
    }

# ----------------------------
# SEARCH API (SCHEMES ENGINE)
# ----------------------------
@app.post("/search")
def search(data: SearchRequest):
    results = search_schemes(data.query, data.filters)

    return {
        "query": data.query,
        "filters": data.filters,
        "results": results
    }

# ----------------------------
# CHAT API (AI ENGINE)
# ----------------------------
@app.post("/chat")
def chat(data: ChatRequest):
    return chat_with_ai(
        message=data.message,
        user_id=data.user_id
    )