from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
from geopy.distance import geodesic
import uvicorn


Base = declarative_base()

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    country = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

# Pydantic model for address data
class AddressCreate(BaseModel):
    street: str
    city: str
    country: str
    latitude: float
    longitude: float

class AddressResponse(BaseModel):
    id: int
    street: str
    city: str
    country: str
    latitude: float
    longitude: float

# FastAPI instance
app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///.sample.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
def create_address(db, address: AddressCreate):
    db.add(Address(**address.dict()))
    db.commit()
    db.refresh(address)
    return address

def get_address(db, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()

def get_addresses(db, skip: int = 0, limit: int = 10):
    return db.query(Address).offset(skip).limit(limit).all()

def delete_address(db, address_id: int):
    address = db.query(Address).filter(Address.id == address_id).first()
    if address:
        db.delete(address)
        db.commit()
        return {"message": "Address deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Address not found")

def get_addresses_within_distance(db, latitude: float, longitude: float, distance: float):
    addresses = db.query(Address).all()
    nearby_addresses = []
    for address in addresses:
        address_coordinates = (address.latitude, address.longitude)
        given_coordinates = (latitude, longitude)
        if geodesic(address_coordinates, given_coordinates).kilometers <= distance:
            nearby_addresses.append(address)
    return nearby_addresses

# API endpoints
@app.post("/addresses/", response_model=AddressResponse)
def create_new_address(address: AddressCreate, db: SessionLocal = Depends(get_db)):
    return create_address(db, address)

@app.get("/addresses/{address_id}", response_model=AddressResponse)
def read_address(address_id: int, db: SessionLocal = Depends(get_db)):
    address = get_address(db, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.get("/addresses/", response_model=List[AddressResponse])
def read_addresses(skip: int = 0, limit: int = 10, db: SessionLocal = Depends(get_db)):
    return get_addresses(db, skip, limit)

@app.delete("/addresses/{address_id}")
def delete_address_by_id(address_id: int, db: SessionLocal = Depends(get_db)):
    return delete_address(db, address_id)

@app.get("/addresses/nearby/")
def get_addresses_nearby(latitude: float, longitude: float, distance: float, db: SessionLocal = Depends(get_db)):
    return get_addresses_within_distance(db, latitude, longitude, distance)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
