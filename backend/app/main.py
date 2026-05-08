from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

from sqlalchemy.orm import Session

from app.database.db import engine, SessionLocal, Base
from app.models.scheme_model import Scheme

from app.routes import schemes, ai
from app.routes.voice import router as voice_router
from app.routes.brain import router as brain_router

from app.services.scheme_service import search_schemes
from app.services.ai_service import chat_with_ai

# =====================================================
# APP INIT
# =====================================================
app = FastAPI(
    title="Bandhu AI",
    description="Govt Schemes + Voice + Brain AI Agent",
    version="4.0.0"
)

# =====================================================
# CORS (FRONTEND CONNECTION FIXED)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# ROUTES (MODULAR SYSTEM)
# =====================================================
app.include_router(brain_router)
app.include_router(voice_router)
app.include_router(schemes.router)
app.include_router(ai.router)

# =====================================================
# DATABASE INIT
# =====================================================
def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Scheme).count() == 0:
            db.add_all([
                Scheme(name="PM Kisan", min_age=18, max_income=500000),
                Scheme(name="Scholarship Yojana", min_age=17, max_income=300000),
                Scheme(name="Farmer Support", min_age=21, max_income=400000),
            ])
            db.commit()
    finally:
        db.close()

init_db()

# =====================================================
# REQUEST MODELS
# =====================================================
class SearchRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = {}

class ChatRequest(BaseModel):
    user_id: Optional[str] = "default"
    message: str

class EligibilityRequest(BaseModel):
    age: int
    income: int
    category: Optional[str] = "general"

# =====================================================
# CORE ENDPOINTS
# =====================================================
@app.get("/")
def home():
    return {
        "status": "Bandhu AI Running 🚀",
        "version": "4.0.0",
        "modules": ["voice", "brain", "schemes", "chat"]
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "system": "bandhu-ai-core"
    }

# =====================================================
# SCHEMES (ALL SCHEMES)
# =====================================================
@app.get("/schemes")
def get_schemes():
    db = SessionLocal()
    try:
        return {
            "schemes": [s.to_dict() for s in db.query(Scheme).all()]
        }
    finally:
        db.close()

# =====================================================
# 🧠 MAIN UI ENDPOINT (IMPORTANT FOR YOUR REACT APP)
# =====================================================
@app.post("/schemes/eligible")
def eligible_schemes(data: EligibilityRequest):
    db = SessionLocal()
    try:
        schemes = db.query(Scheme).filter(
            Scheme.min_age <= data.age,
            Scheme.max_income >= data.income
        ).all()

        results = []

        for s in schemes:
            results.append({
                "name": s.name,
                "benefit": "As per scheme rules",
                "reason": f"Age ≥ {data.age}, Income ≤ {data.income}"
            })

        explanation = (
            f"You are eligible based on age {data.age}, "
            f"income {data.income}, and category {data.category}."
        )

        return {
            "schemes": results,
            "explanation": explanation
        }

    finally:
        db.close()

# =====================================================
# SEARCH ENGINE
# =====================================================
@app.post("/search")
def search(data: SearchRequest):
    results = search_schemes(data.query, data.filters)

    return {
        "query": data.query,
        "results": results
    }

# =====================================================
# CHAT AI CORE
# =====================================================
@app.post("/chat")
def chat(data: ChatRequest):
    return chat_with_ai(
        message=data.message,
        user_id=data.user_id
    )