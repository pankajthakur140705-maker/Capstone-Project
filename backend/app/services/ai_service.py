import re
from typing import Dict, List
from app.services.scheme_service import search_schemes


# -----------------------------
# EXTRACT INFO FROM USER TEXT
# -----------------------------
def extract_filters(text: str) -> Dict:
    text = text.lower()

    filters = {}

    # age detection
    age_match = re.search(r'(\d{1,2})\s*(years|year|yo|age)?', text)
    if age_match:
        age = int(age_match.group(1))
        if 0 < age < 100:
            filters["age"] = age

    # income detection (simple logic)
    income_match = re.search(r'(\d+)\s*(lakh|lakhs|k|thousand)?', text)
    if income_match:
        income = int(income_match.group(1))

        if "lakh" in text:
            income *= 100000
        elif "k" in text or "thousand" in text:
            income *= 1000

        filters["income"] = income

    return filters


# -----------------------------
# INTENT DETECTION
# -----------------------------
def detect_intent(text: str) -> str:
    text = text.lower()

    if any(word in text for word in ["eligible", "can i apply", "am i eligible"]):
        return "eligibility"

    if any(word in text for word in ["suggest", "recommend", "best scheme"]):
        return "recommendation"

    return "search"


# -----------------------------
# FORMAT RESPONSE (IMPORTANT)
# -----------------------------
def format_response(schemes: List[dict]) -> str:
    if not schemes:
        return "❌ No matching schemes found."

    response = "🎯 Here are the best schemes for you:\n\n"

    for s in schemes[:5]:
        response += (
            f"👉 {s.get('name')}\n"
            f"   🏷 Category: {s.get('category')}\n"
            f"   📄 {s.get('description')}\n\n"
        )

    return response


# -----------------------------
# MAIN AI CHAT ENGINE
# -----------------------------
def chat_with_ai(user_text: str):

    # 1. extract filters from natural language
    filters = extract_filters(user_text)

    # 2. detect intent
    intent = detect_intent(user_text)

    # 3. run scheme search
    results = search_schemes(user_text, filters)

    # 4. format smart response
    response = format_response(results)

    return {
        "intent": intent,
        "filters": filters,
        "results": results,
        "response": response
    }
    from app.services.scheme_service import search_schemes

def generate_chat_response(message: str):

    message_lower = message.lower()

    # detect intent
    if "scheme" in message_lower or "help" in message_lower:
        schemes = search_schemes(message, {})

        return {
            "type": "scheme_recommendation",
            "response": "Here are the best schemes for you:",
            "data": schemes
        }

    # fallback AI response
    return {
        "type": "chat",
        "response": f"I understand: {message}. I will help you with schemes, jobs, and benefits."
    }