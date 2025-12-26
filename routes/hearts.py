from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Heart, HeartStatus

router = APIRouter(prefix="/hearts")

def db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/send")
def send_heart(senderId: str, receiverId: str, db: Session = Depends(db)):
    heart = Heart(senderId=senderId, receiverId=receiverId)
    db.add(heart)
    db.commit()
    db.refresh(heart)
    return {"success": True, "status": heart.status}

@router.get("/{userId}/sent")
def get_sent(userId: str, db: Session = Depends(db)):
    return db.query(Heart).filter(Heart.senderId == userId).all()

@router.get("/{userId}/received")
def get_received(userId: str, db: Session = Depends(db)):
    return db.query(Heart).filter(Heart.receiverId == userId).all()

@router.post("/accept")
def accept(senderId: str, receiverId: str, db: Session = Depends(db)):
    heart = db.query(Heart).filter(Heart.senderId==senderId, Heart.receiverId==receiverId).first()
    heart.status = HeartStatus.accepted
    db.commit()
    return {"message": "accepted ❤️"}
