from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, marketplace, assistant

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LivestockLink AI Backend")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(marketplace.router, prefix="/marketplace", tags=["Marketplace"])
app.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])

@app.get("/")
def root():
    return {"message": "LivestockLink AI Backend Running"}