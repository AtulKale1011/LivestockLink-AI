from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./livestock.db")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DISEASE_SERVICE_URL = os.getenv("DISEASE_SERVICE_URL", "http://localhost:8001")
PRICE_SERVICE_URL = os.getenv("PRICE_SERVICE_URL", "http://localhost:8002")