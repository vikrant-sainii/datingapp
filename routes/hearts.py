from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Heart, Mutual, HeartStatus
from database import get_db

router = APIRouter(prefix="/hearts", tags=["Hearts"])

# -------------------------
# SEND HEART
# -------------------------
@router.post("/send")
def send_heart(senderId: str, receiverId: str, db: Session = Depends(get_db)):
    existing = db.query(Heart).filter(
        Heart.senderId == senderId, Heart.receiverId == receiverId
    ).first()

    if existing:
        return {"message": "Already sent", "status": existing.status.value}

    heart = Heart(senderId=senderId, receiverId=receiverId)
    db.add(heart)
    db.commit()
    return {"message": "Heart sent ❤️", "status": "pending"}


# -------------------------
# ACCEPT HEART → Check Mutual
# -------------------------
@router.post("/accept")
def accept_heart(senderId: str, receiverId: str, db: Session = Depends(get_db)):
    heart = db.query(Heart).filter(
        Heart.senderId == senderId, Heart.receiverId == receiverId
    ).first()

    if not heart:
        raise HTTPException(404, "No heart found")

    heart.status = HeartStatus.accepted
    db.commit()

    # Check mutual like
    reverse = db.query(Heart).filter(
        Heart.senderId == receiverId, Heart.receiverId == senderId
    ).first()

    if reverse and reverse.status == HeartStatus.accepted:
        db.add(Mutual(userA=senderId, userB=receiverId))
        db.commit()
        return {"message": "💞 MATCHED!", "chatUnlocked": True}

    return {"message": "Accepted ❤️", "status": "accepted"}


# -------------------------
# DECLINE
# -------------------------
@router.post("/decline")
def decline(senderId: str, receiverId: str, db: Session = Depends(get_db)):
    heart = db.query(Heart).filter(
        Heart.senderId == senderId, Heart.receiverId == receiverId
    ).first()

    if not heart:
        raise HTTPException(404, "No request found")

    heart.status = HeartStatus.declined
    db.commit()
    return {"message": "Declined ❌", "status": "declined"}


# -------------------------
# FETCH LISTS
# -------------------------
@router.get("/{user_id}/sent")
def sent_hearts(user_id: str, db: Session = Depends(get_db)):
    return db.query(Heart).filter(Heart.senderId == user_id).all()

@router.get("/{user_id}/received")
def received_hearts(user_id: str, db: Session = Depends(get_db)):
    return db.query(Heart).filter(Heart.receiverId == user_id).all()

@router.get("/{user_id}/mutual")
def mutual(user_id: str, db: Session = Depends(get_db)):
    return db.query(Mutual).filter(
        (Mutual.userA == user_id) | (Mutual.userB == user_id)
    ).all()
