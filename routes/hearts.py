# routes/hearts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Heart
from schemas import HeartCreate, HeartOut

router = APIRouter(prefix="/hearts", tags=["Hearts"])

# Send heart
@router.post("/send", response_model=HeartOut)
def send_heart(data: HeartCreate, db: Session = Depends(get_db)):
    heart = Heart(**data.dict())
    db.add(heart)
    db.commit()
    db.refresh(heart)
    return heart

# Get sent hearts of user
@router.get("/{user_id}/sent")
def get_sent(user_id: str, db: Session = Depends(get_db)):
    return db.query(Heart).filter(Heart.senderId == user_id).all()

# Get received hearts of user
@router.get("/{user_id}/received")
def get_received(user_id: str, db: Session = Depends(get_db)):
    return db.query(Heart).filter(Heart.receiverId == user_id).all()
