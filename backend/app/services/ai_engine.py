from typing import Dict, List, Any
from app.services.scheme_service import search_schemes


# -----------------------------
# MEMORY ANALYZER
# -----------------------------
def build_context(messages: List[str]) -> str:
    return " | ".join(messages[-5:])


# -----------------------------
# PROFILE EXTRACTION (RULE + AI HYBRID)
# -----------------------------
def extract_user_profile(message: str) -> Dict:
    msg = message.lower()

    profile = {
        "age": None,
        "income": None,
        "is_student": False,
        "is_farmer": False
    }

    # age detection
    words = msg.split()
    for i, w in enumerate(words):
        if w.isdigit():
            val = int(w)
            if 10 <= val <= 100:
                profile["age"] = val

    # income detection (simple upgrade)
    if "low income" in msg:
        profile["income"] = 200000
    elif "medium income" in msg:
        profile["income"] = 500000
    elif "high income" in msg:
        profile["income"] = 1000000

    # role detection
    if "student" in msg:
        profile["is_student"] = True

    if "farmer" in msg or "farming" in msg:
        profile["is_farmer"] = True

    return profile


# -----------------------------
# AI EXPLANATION ENGINE
# -----------------------------
def explain_scheme(scheme: Dict, profile: Dict) -> str:
    reasons = []

    if profile.get("age"):
        if scheme.get("min_age", 0) <= profile["age"]:
            reasons.append("matches your age")

    if profile.get("income"):
        if profile["income"] <= scheme.get("max_income", 10**9):
            reasons.append("fits your income level")

    if profile.get("is_student") and "education" in scheme.get("category", "").lower():
        reasons.append("designed for students")

    if profile.get("is_farmer") and "agri" in scheme.get("category", "").lower():
        reasons.append("supports farmers")

    return "Recommended because " + ", ".join(reasons) if reasons else "General match"