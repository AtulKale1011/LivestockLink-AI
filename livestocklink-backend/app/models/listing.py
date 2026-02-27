from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    animal_type = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    location = Column(String)
    owner_id = Column(Integer)