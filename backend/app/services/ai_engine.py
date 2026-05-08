from typing import List, Dict, Any, Optional
import math
from datetime import datetime


# =====================================================
# 🧠 USER INTENT + PROFILE DETECTION ENGINE
# =====================================================
def detect_user_profile(message: str) -> str:
    msg = message.lower()

    profiles = {
        "student": ["student", "study", "college", "school", "scholarship"],
        "farmer": ["farmer", "farming", "crop", "agriculture"],
        "job_seeker": ["job", "unemployed", "work", "employment"],
        "business": ["business", "startup", "self-employed", "entrepreneur"]
    }

    for profile, keywords in profiles.items():
        if any(k in msg for k in keywords):
            return profile

    return "general"


# =====================================================
# 🧠 FEATURE SCORING ENGINE (MULTI-FACTOR AI RANKING)
# =====================================================
def score_scheme(user: Dict[str, Any], scheme: Dict[str, Any], profile: str):

    age = user.get("age", 0)
    income = user.get("income", 10**9)

    min_age = scheme.get("min_age", 0)
    max_income = scheme.get("max_income", 10**9)

    score = 0
    reasons = []

    # -------------------------
    # AGE FIT (30%)
    # -------------------------
    if age >= min_age:
        score += 30
        reasons.append("Eligible age range matched")
    else:
        penalty = (min_age - age) * 2
        score += max(0, 30 - penalty)
        reasons.append(f"Age gap detected: {min_age - age}")

    # -------------------------
    # INCOME FIT (30%)
    # -------------------------
    if income <= max_income:
        score += 30
        reasons.append("Income eligibility satisfied")
    else:
        overflow = income - max_income
        penalty = min(30, overflow / 10000)
        score += max(0, 30 - penalty)
        reasons.append("Income slightly above limit")

    # -------------------------
    # PROFILE BOOST (20%)
    # -------------------------
    profile_weights = {
        "student": 18,
        "farmer": 20,
        "job_seeker": 17,
        "business": 15,
        "general": 10
    }

    score += profile_weights.get(profile, 10)
    reasons.append(f"Profile boost: {profile}")

    # -------------------------
    # SCHEME PRIORITY (10%)
    # -------------------------
    priority_boost = scheme.get("priority", 5)
    score += priority_boost
    reasons.append("Government priority boost applied")

    # -------------------------
    # FINAL NORMALIZATION
    # -------------------------
    confidence = max(0, min(100, round(score, 2)))

    return {
        "scheme": scheme.get("name"),
        "score": confidence,
        "profile": profile,
        "reasons": reasons
    }


# =====================================================
# 🧠 EXPLANATION ENGINE (UI READY AI RESPONSE)
# =====================================================
def generate_explanation(best: Dict[str, Any]) -> str:

    if not best:
        return "No matching schemes found."

    return (
        f"You are identified as a '{best['profile']}' profile. "
        f"Your best matching scheme is '{best['scheme']}' "
        f"with AI confidence score of {best['score']}/100. "
        f"This recommendation is based on eligibility, income fit, and profile analysis."
    )


# =====================================================
# 🧠 MAIN AI GOVERNMENT SCHEME BRAIN ENGINE (LEVEL 10)
# =====================================================
def rank_schemes(
    user: Dict[str, Any],
    schemes: List[Dict[str, Any]],
    message: Optional[str] = ""
):

    profile = detect_user_profile(message or "")

    results = []

    for scheme in schemes:
        results.append(score_scheme(user, scheme, profile))

    # sort by AI score
    results.sort(key=lambda x: x["score"], reverse=True)

    # ranking
    for i, r in enumerate(results):
        r["rank"] = i + 1

    best = results[0] if results else None

    return {
        "engine": "Bandhu AI Govt Scheme Brain v10",
        "timestamp": datetime.utcnow().isoformat(),

        # user understanding
        "detected_profile": profile,

        # results
        "total_schemes_analyzed": len(schemes),
        "ranked_schemes": results,

        # best decision
        "best_match": best,

        # UI READY OUTPUT (IMPORTANT)
        "ui_payload": {
            "top_scheme": best,
            "all_ranked": results
        },

        # human explanation
        "ai_explanation": generate_explanation(best)
    }