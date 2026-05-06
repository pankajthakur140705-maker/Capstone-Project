from sentence_transformers import SentenceTransformer
from typing import Dict, List
import numpy as np
import json

# ⚡ Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

SCHEME_EMBEDDINGS = {}
QUERY_CACHE = {}


# -----------------------------
# LOAD SCHEMES
# -----------------------------
def get_all_schemes():
    with open("app/data/schemes.json", "r") as f:
        return json.load(f)


# -----------------------------
# TEXT BUILDER
# -----------------------------
def build_scheme_text(scheme: dict) -> str:
    return " ".join([
        scheme.get("name", ""),
        scheme.get("category", ""),
        scheme.get("description", ""),
        " ".join(scheme.get("keywords", []))
    ]).lower()


# -----------------------------
# INIT EMBEDDINGS
# -----------------------------
def init_embeddings(schemes: List[dict]):
    global SCHEME_EMBEDDINGS
    SCHEME_EMBEDDINGS = {}

    for s in schemes:
        SCHEME_EMBEDDINGS[s["name"]] = model.encode(build_scheme_text(s))


# -----------------------------
# COSINE SIMILARITY
# -----------------------------
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


# -----------------------------
# SEMANTIC SCORE
# -----------------------------
def semantic_score(query_vec, scheme_name: str):
    scheme_vec = SCHEME_EMBEDDINGS.get(scheme_name)
    if scheme_vec is None:
        return 0.0
    return cosine_similarity(query_vec, scheme_vec)


# -----------------------------
# FILTER SCORE
# -----------------------------
def filter_score(scheme: dict, filters: Dict):
    score = 0

    age = filters.get("age")
    income = filters.get("income")

    if age is not None:
        if scheme.get("min_age", 0) <= age <= scheme.get("max_age", 100):
            score += 15
        else:
            score -= 10

    if income is not None:
        if income <= scheme.get("max_income", float("inf")):
            score += 15
        else:
            score -= 15

    return score


# -----------------------------
# KEYWORD SCORE
# -----------------------------
def keyword_score(query: str, scheme: dict):
    q_words = set(query.lower().split())
    s_words = set(build_scheme_text(scheme).split())
    return len(q_words & s_words) * 5


# -----------------------------
# PROFILE BOOST (FIXED)
# -----------------------------
def profile_boost(scheme: dict, profile: dict):
    score = 0

    if not profile:
        return 0

    if profile.get("is_student") and scheme.get("category") == "Education":
        score += 20

    if profile.get("is_farmer") and scheme.get("category") == "Agriculture":
        score += 25

    if profile.get("income") and profile["income"] <= scheme.get("max_income", 10**9):
        score += 10

    if profile.get("age"):
        if scheme.get("min_age", 0) <= profile["age"] <= scheme.get("max_age", 100):
            score += 10

    return score


# -----------------------------
# MAIN SEARCH ENGINE (FINAL FIXED)
# -----------------------------
def search_schemes(query: str, filters: Dict = {}, profile: Dict = None):

    schemes = get_all_schemes()

    if not SCHEME_EMBEDDINGS:
        init_embeddings(schemes)

    if query not in QUERY_CACHE:
        QUERY_CACHE[query] = model.encode(query.lower())

    query_vec = QUERY_CACHE[query]

    results = []

    for scheme in schemes:

        name = scheme.get("name", "")

        semantic = semantic_score(query_vec, name) * 100
        keyword = keyword_score(query, scheme)
        filters_score = filter_score(scheme, filters)
        priority = scheme.get("priority", 0) * 2
        profile_score = profile_boost(scheme, profile or {})

        total_score = semantic + keyword + filters_score + priority + profile_score

        results.append({
            "scheme": scheme,
            "score": round(total_score, 2)
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return [r["scheme"] for r in results]