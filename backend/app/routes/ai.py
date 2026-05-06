from fastapi import APIRouter
from typing import Dict, List, Any

from app.services.scheme_service import search_schemes
from app.services.ai_engine import extract_user_profile, explain_scheme

router = APIRouter()

# -----------------------------
# MEMORY (replace with DB later)
# -----------------------------
user_memory: Dict[str, List[str]] = {}


# -----------------------------
# INTENT DETECTION ENGINE
# -----------------------------
def detect_intent(message: str) -> str:
    msg = message.lower()

    scheme_keywords = [
        "scheme", "schemes", "yojana", "subsidy",
        "benefit", "loan", "support", "government"
    ]

    farmer_keywords = [
        "farmer", "agriculture", "farming", "crop", "field"
    ]

    if any(w in msg for w in farmer_keywords):
        return "farmer"

    if any(w in msg for w in scheme_keywords):
        return "scheme"

    return "chat"


# -----------------------------
# FORMAT SCHEME OUTPUT
# -----------------------------
def format_schemes(schemes: List[dict], profile: Dict) -> List[dict]:
    formatted = []

    for s in schemes[:5]:
        formatted.append({
            "name": s.get("name"),
            "category": s.get("category"),
            "description": s.get("description"),
            "eligibility_reason": explain_scheme(s, profile)
        })

    return formatted


# -----------------------------
# MEMORY HANDLER (SAFE)
# -----------------------------
def update_memory(user_id: str, message: str):
    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append(message)

    # keep only last 5 messages (context window)
    user_memory[user_id] = user_memory[user_id][-5:]


def get_context(user_id: str) -> str:
    return " ".join(user_memory.get(user_id, []))


# -----------------------------
# MAIN CHAT ENDPOINT
# -----------------------------
@router.post("/chat")
def chat(data: Dict[str, Any]):

    user_id = data.get("user_id", "default")
    message = data.get("message", "").strip()

    if not message:
        return {
            "type": "chat",
            "response": "Please enter a message.",
            "data": []
        }

    # ---------------- MEMORY ----------------
    update_memory(user_id, message)
    context = get_context(user_id)

    # ---------------- PROFILE EXTRACTION ----------------
    profile = extract_user_profile(context + " " + message)

    # ---------------- INTENT ----------------
    intent = detect_intent(message)

    # ---------------- SCHEME MODE ----------------
    if intent in ["scheme", "farmer"]:

        query = message

        if intent == "farmer":
            profile["is_farmer"] = True
            query += " agriculture subsidy farming government"

        results = search_schemes(query, profile)

        return {
            "type": "scheme_recommendation",
            "response": "AI analyzed your profile and found the best matching schemes.",
            "profile": profile,
            "data": format_schemes(results, profile)
        }

    # ---------------- CHAT MODE ----------------
    return {
        "type": "chat",
        "response": (
            "I can help you find government schemes based on your age, income, and situation. "
            "Try: 'I am a 20 year old student with low income'"
        ),
        "profile": profile,
        "data": []
    }