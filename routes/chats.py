# routes/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ChatMessage
from schemas import ChatMessageCreate, ChatMessageOut

router = APIRouter(prefix="/chat", tags=["Chat"])

# Generate consistent chat room id: userA_userB
def chat_room(id1: str, id2: str):
    return "_".join(sorted([id1, id2]))


# 📌 Send a chat message (only for mutuals)
@router.post("/send", response_model=ChatMessageOut)
def send_message(message: ChatMessageCreate, db: Session = Depends(get_db)):
    room_id = chat_room(message.senderId, message.receiverId)
    msg = ChatMessage(
        roomId=room_id,
        senderId=message.senderId,
        receiverId=message.receiverId,
        text=message.text,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


# 📌 Get all messages between two users
@router.get("/{user1}/{user2}", response_model=list[ChatMessageOut])
def get_chat_history(user1: str, user2: str, db: Session = Depends(get_db)):
    room_id = chat_room(user1, user2)
    messages = db.query(ChatMessage).filter(ChatMessage.roomId == room_id).all()
    return messages
