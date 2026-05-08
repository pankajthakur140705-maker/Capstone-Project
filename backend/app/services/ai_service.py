import os
import re
from typing import Dict, List

from dotenv import load_dotenv
import google.generativeai as genai

from app.services.scheme_service import search_schemes


# =====================================================
# LOAD ENV
# =====================================================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


# =====================================================
# FILTER EXTRACTION
# =====================================================
def extract_filters(text: str) -> Dict:

    text = text.lower()
    filters = {}

    # AGE
    age_match = re.search(r'(\d{1,2})\s*(years|year|yo|age)?', text)
    if age_match:
        age = int(age_match.group(1))
        if 0 < age < 100:
            filters["age"] = age

    # INCOME
    income_match = re.search(r'(\d+)\s*(lakh|lakhs|k|thousand)?', text)
    if income_match:
        income = int(income_match.group(1))

        if "lakh" in text:
            income *= 100000
        elif "k" in text or "thousand" in text:
            income *= 1000

        filters["income"] = income

    # CATEGORY
    if "farmer" in text:
        filters["category"] = "Agriculture"
    elif "student" in text:
        filters["category"] = "Education"
    elif "woman" in text or "women" in text:
        filters["category"] = "Women"
    elif "job" in text or "employment" in text:
        filters["category"] = "Employment"

    return filters


# =====================================================
# INTENT DETECTION
# =====================================================
def detect_intent(text: str) -> str:

    text = text.lower()

    if any(w in text for w in ["hello", "hi", "hey"]):
        return "greeting"

    if any(w in text for w in ["eligible", "am i eligible", "can i apply"]):
        return "eligibility"

    if any(w in text for w in ["recommend", "best scheme", "suggest"]):
        return "recommendation"

    if any(w in text for w in ["scheme", "help", "support"]):
        return "search"

    return "general"


# =====================================================
# GREETING RESPONSE
# =====================================================
def greeting_response():

    return {
        "type": "chat",
        "response": (
            "👋 Hello! I am Bandhu AI.\n\n"
            "I can help you with:\n"
            "• Government schemes\n"
            "• Scholarships\n"
            "• Farmer support\n"
            "• Jobs & Employment\n"
            "• Eligibility checking"
        )
    }


# =====================================================
# SCHEME CONTEXT BUILDER
# =====================================================
def build_scheme_context(schemes: List[dict]) -> str:

    if not schemes:
        return "No schemes found."

    context = ""

    for s in schemes[:5]:
        context += f"""
Name: {s.get('name')}
Category: {s.get('category')}
Description: {s.get('description')}
---

"""
    return context


# =====================================================
# GEMINI RESPONSE ENGINE
# =====================================================
def generate_ai_response(user_message: str, schemes: List[dict], filters: Dict, intent: str):

    scheme_context = build_scheme_context(schemes)

    prompt = f"""
You are Bandhu AI — a helpful Indian government scheme assistant.

Your job:
- Help users find schemes
- Explain eligibility simply
- Suggest best schemes
- Speak like a friendly AI assistant

INTENT: {intent}
FILTERS: {filters}

AVAILABLE SCHEMES:
{scheme_context}

USER MESSAGE:
{user_message}

Rules:
- Simple English
- Short clear answers
- Be helpful and practical
"""

    response = model.generate_content(prompt)

    return response.text


# =====================================================
# MAIN CHAT ENGINE (USED BY FRONTEND + VOICE)
# =====================================================
def chat_with_ai(message: str, user_id: str = "default"):

    try:

        text = message.strip()

        intent = detect_intent(text)

        # GREETING
        if intent == "greeting":
            return greeting_response()

        filters = extract_filters(text)

        results = search_schemes(text, filters)

        ai_response = generate_ai_response(
            user_message=text,
            schemes=results,
            filters=filters,
            intent=intent
        )

        return {
            "type": "ai_chat",
            "intent": intent,
            "filters": filters,
            "response": ai_response,
            "data": results
        }

    except Exception as e:

        print("AI ERROR:", e)

        return {
            "type": "chat",
            "response": "⚠️ AI temporarily unavailable. Try again.",
            "error": str(e)
        }


# =====================================================
# VOICE AI ENTRY POINT (IMPORTANT FOR YOUR FRONTEND)
# =====================================================
def get_ai_response(text: str):

    text = text.lower()

    if "scheme" in text:
        return "I can help you find government schemes. Tell me your age and income."

    if "eligibility" in text:
        return "Tell me your age and income, I will check eligibility."

    if "hello" in text:
        return "Hello! I am Bandhu AI voice assistant."

    return chat_with_ai(text)["response"]