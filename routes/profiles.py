# routes/profiles.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Profile
from schemas import ProfileCreate, ProfileOut

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileOut)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    p = Profile(**profile.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/{user_id}", response_model=ProfileOut)
def get_profile(user_id: str, db: Session = Depends(get_db)):
    p = db.query(Profile).filter(Profile.id == user_id).first()
    if not p:
        return {"error": "Profile not found"}
    return p

@router.get("/")
def list_profiles(db: Session = Depends(get_db)):
    return db.query(Profile).all()
