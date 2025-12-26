from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Profile

router = APIRouter(prefix="/profiles")

def db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/")
def save_profile(id: str, name: str, branch: str, year: str, avatar: str, db: Session = Depends(db)):
    profile = Profile(id=id, name=name, branch=branch, year=year, avatar=avatar)
    db.merge(profile)
    db.commit()
    return {"saved": id}

@router.get("/{id}")
def get_profile(id: str, db: Session = Depends(db)):
    return db.query(Profile).filter(Profile.id == id).first()
