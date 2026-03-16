from fastapi import FastAPI
from pydantic import BaseModel
from app.hybrid_engine import predict_livestock_price

app = FastAPI()


class PredictionRequest(BaseModel):
    district: str
    animal_type: str
    quantity: int
    weight_per_unit: float | None = None
    age_months: int | None = None
    quality_grade: str = "medium"


@app.post("/predict")
def predict(request: PredictionRequest):
    return predict_livestock_price(
        district=request.district,
        animal_type=request.animal_type,
        quantity=request.quantity,
        weight_per_unit=request.weight_per_unit,
        age_months=request.age_months,
        quality_grade=request.quality_grade
    )