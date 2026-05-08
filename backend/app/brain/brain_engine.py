from typing import Dict, Any
from app.services.ai_service import chat_with_ai
from app.services.scheme_service import search_schemes


# ==============================
# MEMORY (simple in-memory brain)
# ==============================
USER_MEMORY = {}


def get_memory(user_id: str):
    return USER_MEMORY.get(user_id, {})


def update_memory(user_id: str, key: str, value: Any):
    if user_id not in USER_MEMORY:
        USER_MEMORY[user_id] = {}

    USER_MEMORY[user_id][key] = value


# ==============================
# INTENT CLASSIFIER (BRAIN)
# ==============================
def detect_intent(message: str) -> str:

    msg = message.lower()

    if "scheme" in msg or "yojana" in msg:
        return "SCHEME_SEARCH"

    if "age" in msg and "income" in msg:
        return "ELIGIBILITY"

    if "hello" in msg or "hi" in msg:
        return "GREETING"

    return "CHAT"


# ==============================
# MAIN BRAIN FUNCTION
# ==============================
def brain(user_id: str, message: str, metadata: Dict = None):

    intent = detect_intent(message)

    memory = get_memory(user_id)

    # --------------------------
    # 1. SCHEME SEARCH TOOL
    # --------------------------
    if intent == "SCHEME_SEARCH":
        result = search_schemes(message, {})

        return {
            "type": "tool",
            "intent": intent,
            "response": result
        }

    # --------------------------
    # 2. CHAT (LLM MODE)
    # --------------------------
    elif intent == "CHAT":
        response = chat_with_ai(
            message=message,
            user_id=user_id
        )

        update_memory(user_id, "last_message", message)

        return {
            "type": "ai",
            "intent": intent,
            "response": response.get("response", response)
        }

    # --------------------------
    # 3. GREETING
    # --------------------------
    elif intent == "GREETING":
        return {
            "type": "system",
            "intent": intent,
            "response": "Hello 👋 I am Bandhu AI, your assistant."
        }

    # --------------------------
    # DEFAULT FALLBACK
    # --------------------------
    return {
        "type": "fallback",
        "intent": intent,
        "response": "I did not understand. Can you rephrase?"
    }