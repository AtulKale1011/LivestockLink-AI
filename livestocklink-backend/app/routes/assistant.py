from fastapi import APIRouter
from app.services.ml_client import call_price_service

router = APIRouter()

@router.post("/query")
def assistant_query(question: str):
    if "price" in question.lower():
        result = call_price_service({"animal": "goat", "region": "maharashtra"})
        return {"response": result}
    
    return {
        "response": "For disease diagnosis, please upload image in disease section."
    }