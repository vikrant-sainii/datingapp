# routes/hearts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Heart, Mutual, HeartStatus
from database import get_db

router = APIRouter(prefix="/hearts", tags=["Hearts"])

# Send Heart
@router.post("/send")
def send_heart(senderId: str, receiverId: str, db: Session = Depends(get_db)):
    heart = Heart(senderId=senderId, receiverId=receiverId)
    db.add(heart)
    db.commit()
    return {"message": "Heart sent ❤️", "data": heart.id}

# Accept Heart -> moves to mutuals list
@router.post("/accept")
def accept_heart(senderId: str, receiverId: str, db: Session = Depends(get_db)):
    heart = db.query(Heart).filter(
        Heart.senderId == senderId, Heart.receiverId == receiverId
    ).first()
    if not heart:
        return {"error": "No heart found"}

    heart.status = HeartStatus.accepted
    db.add(Mutual(userA=senderId, userB=receiverId))
    db.commit()
    return {"message": "Matched! 💗 Chat Unlocked"}

# Decline
@router.post("/decline")
def decline_heart(senderId: str, receiverId: str, db: Session = Depends(get_db)):
    heart = db.query(Heart).filter(
        Heart.senderId == senderId, Heart.receiverId == receiverId
    ).first()
    if not heart:
        return {"error": "No request found"}
    heart.status = HeartStatus.declined
    db.commit()
    return {"message": "Declined ❌"}

# Sent Requests
@router.get("/{user_id}/sent")
def sent_hearts(user_id: str, db: Session = Depends(get_db)):
    return db.query(Heart).filter(Heart.senderId == user_id).all()

# Received Requests
@router.get("/{user_id}/received")
def received_hearts(user_id: str, db: Session = Depends(get_db)):
    return db.query(Heart).filter(Heart.receiverId == user_id).all()

# Mutual Matches
@router.get("/{user_id}/mutual")
def mutual(user_id: str, db: Session = Depends(get_db)):
    return db.query(Mutual).filter(
        (Mutual.userA == user_id) | (Mutual.userB == user_id)
    ).all()
