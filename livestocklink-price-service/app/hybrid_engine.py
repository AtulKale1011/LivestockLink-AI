import pandas as pd
import numpy as np
from datetime import datetime
from app.model_loader import get_model, get_encoders

model = get_model()
district_encoder, animal_encoder = get_encoders()


def adjust_price(base_price, weight, age, quality):

    adjusted_price = base_price

    # Quality adjustment
    if quality == "low":
        adjusted_price *= 0.95
    elif quality == "high":
        adjusted_price *= 1.08

    # Weight adjustment
    if weight is not None:
        optimal_weight = 30
        weight_factor = 1 - abs(weight - optimal_weight) / 100
        adjusted_price *= weight_factor

    # Age adjustment
    if age is not None:
        optimal_age = 12
        age_factor = 1 - abs(age - optimal_age) / 100
        adjusted_price *= age_factor

    return adjusted_price



def calculate_risk_score():
    disease_risk = np.random.uniform(0.05, 0.25)
    climate_risk = np.random.uniform(0.05, 0.3)
    return round((disease_risk + climate_risk) / 2, 2)


def calculate_recommendation_score(profit_margin, risk_score):
    score = (profit_margin * 0.7) + ((1 - risk_score) * 0.3)
    return round(score * 100, 2)



def predict_livestock_price(
    district,
    animal_type,
    quantity,
    weight_per_unit=None,
    age_months=None,
    quality_grade="medium"
):

    now = datetime.now()
    week_of_year = now.isocalendar()[1]
    year = now.year

    district_encoded = district_encoder.transform([district])[0]
    animal_encoded = animal_encoder.transform([animal_type])[0]

    input_data = pd.DataFrame([{
        "district_encoded": district_encoded,
        "animal_encoded": animal_encoded,
        "week_of_year": week_of_year,
        "year": year,
        "feed_cost_index": 1.1,
        "water_availability_index": 1.0,
        "disease_risk_index": 0.1,
        "climate_risk_index": 0.15,
        "festival_flag": 0,
        "export_demand_index": 1
    }])

    base_price = float(model.predict(input_data)[0])

    adjusted_price = adjust_price(
        base_price,
        weight_per_unit,
        age_months,
        quality_grade
    )

    total_revenue = adjusted_price * quantity
    production_cost = total_revenue * 0.65
    total_profit = total_revenue - production_cost
    profit_margin = total_profit / total_revenue

    risk_score = calculate_risk_score()
    recommendation_score = calculate_recommendation_score(
        profit_margin,
        risk_score
    )

    return {
        "base_price_per_unit": float(round(base_price, 2)),
        "adjusted_price_per_unit": float(round(adjusted_price, 2)),
        "total_revenue": float(round(total_revenue, 2)),
        "estimated_production_cost": float(round(production_cost, 2)),
        "total_profit": float(round(total_profit, 2)),
        "profit_margin_percent": float(round(profit_margin * 100, 2)),
        "risk_score": float(risk_score),
        "recommendation_score": float(recommendation_score)
    }