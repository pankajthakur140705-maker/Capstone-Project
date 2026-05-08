from typing import Dict, Any
from app.services.ai_service import chat_with_ai
from app.services.scheme_service import search_schemes


# =========================
# SIMPLE PERSISTENT MEMORY
# =========================
MEMORY = {}


def load_memory(user_id: str):
    return MEMORY.get(user_id, {
        "history": [],
        "facts": {}
    })


def save_memory(user_id: str, memory: dict):
    MEMORY[user_id] = memory


# =========================
# PLANNER (DECISION ENGINE)
# =========================
def planner(message: str) -> str:

    msg = message.lower()

    if any(k in msg for k in ["scheme", "yojana", "benefit"]):
        return "USE_SCHEME_TOOL"

    if any(k in msg for k in ["age", "income", "eligible"]):
        return "USE_ELIGIBILITY_TOOL"

    return "USE_CHAT_LLM"


# =========================
# TOOL EXECUTOR
# =========================
def run_tool(intent: str, message: str):

    if intent == "USE_SCHEME_TOOL":
        return search_schemes(message, {})

    if intent == "USE_ELIGIBILITY_TOOL":
        return search_schemes(message, {})

    return None


# =========================
# AGENT MAIN LOOP
# =========================
def run_agent(user_id: str, message: str) -> Dict[str, Any]:

    memory = load_memory(user_id)

    # 1. Store history
    memory["history"].append(message)

    # 2. PLAN
    action = planner(message)

    # 3. TOOL EXECUTION
    tool_result = run_tool(action, message)

    # 4. GENERATE RESPONSE
    if action == "USE_CHAT_LLM":
        response = chat_with_ai(
            message=message,
            user_id=user_id
        )
    else:
        response = {
            "response": tool_result,
            "type": "tool_result"
        }

    # 5. UPDATE MEMORY
    memory["facts"]["last_intent"] = action
    save_memory(user_id, memory)

    # 6. FINAL OUTPUT
    return {
        "user_id": user_id,
        "intent": action,
        "response": response,
        "memory_state": memory
    }