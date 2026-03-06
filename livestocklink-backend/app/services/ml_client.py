import requests
from app.config import DISEASE_SERVICE_URL, PRICE_SERVICE_URL

def call_disease_service(data: dict):
    try:
        response = requests.post(f"{DISEASE_SERVICE_URL}/predict", json=data)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Disease service failed: {str(e)}"
        }


def call_price_service(data: dict):
    try:
        response = requests.post(f"{PRICE_SERVICE_URL}/predict", json=data)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Price service failed: {str(e)}"
        }