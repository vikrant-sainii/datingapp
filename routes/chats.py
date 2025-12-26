# routes/chats.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import ChatMessage, Mutual
from database import get_db

router = APIRouter(prefix="/chats", tags=["Chats"])

# Send Chat Message
@router.post("/send")
def send_message(senderId: str, receiverId: str, text: str, db: Session = Depends(get_db)):
    # Check if users are mutual
    is_mutual = db.query(Mutual).filter(
        ((Mutual.userA == senderId) & (Mutual.userB == receiverId)) |
        ((Mutual.userA == receiverId) & (Mutual.userB == senderId))
    ).first()

    if not is_mutual:
        return {"error": "Not matched yet. Chat locked 🔒"}

    roomId = "_".join(sorted([senderId, receiverId]))
    message = ChatMessage(roomId=roomId, senderId=senderId, receiverId=receiverId, text=text)
    db.add(message)
    db.commit()
    db.refresh(message)

    return {"message": "Message sent 💬"}

# Get Chat History
@router.get("/{userA}/{userB}")
def get_chat(userA: str, userB: str, db: Session = Depends(get_db)):
    roomId = "_".join(sorted([userA, userB]))
    return db.query(ChatMessage).filter(ChatMessage.roomId == roomId).all()
