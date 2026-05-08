from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.services.scheme_ai_engine import rank_schemes
from app.services.ai_service import chat_with_ai

router = APIRouter(prefix="/brain", tags=["Brain AI"])


# =========================
# REQUEST MODEL
# =========================
class BrainRequest(BaseModel):
    user_id: str = "default"
    message: str

    # optional structured context
    age: Optional[int] = None
    income: Optional[int] = None


# =========================
# INTENT CLASSIFIER (LEVEL 1)
# =========================
def detect_intent(text: str) -> str:
    text = text.lower()

    scheme_keywords = [
        "scheme", "yojana", "benefit",
        "apply", "eligibility", "govt scheme"
    ]

    if any(word in text for word in scheme_keywords):
        return "scheme"

    return "chat"


# =========================
# SIMPLE PARAM EXTRACTOR (FALLBACK)
# =========================
def extract_numbers(text: str):
    import re
    nums = re.findall(r"\d+", text)

    age = None
    income = None

    if len(nums) >= 1:
        age = int(nums[0])

    if len(nums) >= 2:
        income = int(nums[1])

    return age, income


# =========================
# SCHEME MOCK DATA (can move to DB later)
# =========================
MOCK_SCHEMES = [
    {
        "name": "PM Kisan",
        "min_age": 18,
        "max_income": 500000
    },
    {
        "name": "Scholarship Yojana",
        "min_age": 17,
        "max_income": 300000
    },
    {
        "name": "Farmer Support",
        "min_age": 21,
        "max_income": 400000
    }
]


# =========================
# MAIN BRAIN ENGINE
# =========================
@router.post("/process")
def process(req: BrainRequest):

    text = req.message
    intent = detect_intent(text)

    # =====================================================
    # 1. SCHEME INTELLIGENCE ENGINE
    # =====================================================
    if intent == "scheme":

        age, income = req.age, req.income

        # fallback extraction from text
        if age is None or income is None:
            age, income = extract_numbers(text)

        if age is not None and income is not None:

            ranked = rank_schemes(
                {
                    "age": age,
                    "income": income
                },
                MOCK_SCHEMES
            )

            return {
                "type": "scheme_ai",
                "intent": "scheme",
                "input": {
                    "age": age,
                    "income": income
                },
                "response": ranked
            }

        return {
            "type": "scheme_ai",
            "intent": "scheme",
            "response": "Please provide age and income for accurate scheme ranking."
        }

    # =====================================================
    # 2. GENERAL AI CHAT LAYER
    # =====================================================
    ai_response = chat_with_ai(
        message=text,
        user_id=req.user_id
    )

    return {
        "type": "chat_ai",
        "intent": "chat",
        "response": ai_response
    }