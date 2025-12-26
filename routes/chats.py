from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import ChatMessage, Mutual
from database import get_db

router = APIRouter(prefix="/chats", tags=["Chats"])

@router.post("/send")
def send_message(senderId: str, receiverId: str, text: str, db: Session = Depends(get_db)):
    mutual = db.query(Mutual).filter(
        ((Mutual.userA == senderId) & (Mutual.userB == receiverId)) |
        ((Mutual.userA == receiverId) & (Mutual.userB == senderId))
    ).first()

    if not mutual:
        raise HTTPException(403, "Not matched yet 🔒")

    roomId = "_".join(sorted([senderId, receiverId]))
    msg = ChatMessage(roomId=roomId, senderId=senderId, receiverId=receiverId, text=text)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return {"message": "💬 delivered", "roomId": roomId}


@router.get("/{userA}/{userB}")
def get_chat(userA: str, userB: str, db: Session = Depends(get_db)):
    roomId = "_".join(sorted([userA, userB]))
    msgs = db.query(ChatMessage).filter(ChatMessage.roomId == roomId).all()
    return msgs
