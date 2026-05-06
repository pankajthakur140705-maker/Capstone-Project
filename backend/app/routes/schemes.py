from fastapi import APIRouter, Query
from app.services.scheme_service import get_all_schemes
router = APIRouter()

@router.get("/schemes")
def fetch_schemes(category: str = Query(None)):
    schemes = get_all_schemes()
    
    if category:
        schemes = [
            s for s in schemes 
            if s.get("category", "").lower() == category.lower()
        ]
    
    return {
        "count": len(schemes),
        "data": schemes
    }


@router.get("/eligible-schemes")
def eligible(age: int, income: int):
    schemes = get_eligible_schemes(age, income)
    
    return {
        "count": len(schemes),
        "data": schemes
    }