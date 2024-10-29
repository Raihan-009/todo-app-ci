import os

# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List

# Initialize FastAPI app
app = FastAPI(
    title="Name Service",
    description="A simple API to save and retrieve names",
    version="1.0.0"
)

# Database Configuration
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/namesdb")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class NameEntry(Base):
    __tablename__ = "names"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Model for Request/Response
class NameSchema(BaseModel):
    name: str

class NameResponse(BaseModel):
    id: int
    name: str

# Database Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Routes
@app.post("/names/", response_model=NameResponse, tags=["names"])
def create_name(name_entry: NameSchema, db: SessionLocal = next(get_db())):
    """
    Create a new name entry in the database
    """
    db_name = NameEntry(name=name_entry.name)
    db.add(db_name)
    db.commit()
    db.refresh(db_name)
    return db_name

@app.get("/names/", response_model=List[NameResponse], tags=["names"])
def get_names(db: SessionLocal = next(get_db())):
    """
    Retrieve all names from the database
    """
    return db.query(NameEntry).all()

@app.get("/names/{name_id}", response_model=NameResponse, tags=["names"])
def get_name(name_id: int, db: SessionLocal = next(get_db())):
    """
    Retrieve a specific name by ID
    """
    db_name = db.query(NameEntry).filter(NameEntry.id == name_id).first()
    if db_name is None:
        raise HTTPException(status_code=404, detail="Name not found")
    return db_name

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)