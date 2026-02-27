from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.listing import Listing

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_listing(animal_type: str, quantity: int, price: float, location: str, db: Session = Depends(get_db)):
    listing = Listing(
        animal_type=animal_type,
        quantity=quantity,
        price=price,
        location=location,
        owner_id=1
    )
    db.add(listing)
    db.commit()
    return {"message": "Listing created"}

@router.get("/all")
def get_listings(db: Session = Depends(get_db)):
    return db.query(Listing).all()