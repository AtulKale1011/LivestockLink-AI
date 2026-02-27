import requests
from app.config import DISEASE_SERVICE_URL, PRICE_SERVICE_URL

def call_disease_service(data):
    response = requests.post(f"{DISEASE_SERVICE_URL}/predict", json=data)
    return response.json()

def call_price_service(data):
    response = requests.post(f"{PRICE_SERVICE_URL}/forecast", json=data)
    return response.json()