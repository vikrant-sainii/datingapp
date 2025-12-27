from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ChatMessage, AppState

router = APIRouter(prefix="/chats", tags=["Chats"])

# Helper to load JSON state
def get_state(db: Session):
    state = db.query(AppState).first()
    if not state:
        raise HTTPException(500, "AppState missing: run hearts once to initialize backend")
    return state.hearts, state


# ---------------------------------------------------------
# 💬 SEND MESSAGE (Allowed only if mutual match)
# ---------------------------------------------------------
@router.post("/send")
def send_message(senderId: str, receiverId: str, text: str, db: Session = Depends(get_db)):
    data, record = get_state(db)

    # Check if mutual match exists in JSON
    if receiverId not in data["mutual"].get(senderId, []):
        raise HTTPException(status_code=403, detail="Not matched yet 🔒")

    roomId = "_".join(sorted([senderId, receiverId]))
    msg = ChatMessage(roomId=roomId, senderId=senderId, receiverId=receiverId, text=text)

    db.add(msg)
    db.commit()
    db.refresh(msg)

    return {"message": "💬 delivered", "roomId": roomId, "text": text}


# ---------------------------------------------------------
# 📩 GET CHAT HISTORY (Sorted Room)
# ---------------------------------------------------------
@router.get("/{userA}/{userB}")
def get_chat(userA: str, userB: str, db: Session = Depends(get_db)):
    roomId = "_".join(sorted([userA, userB]))
    msgs = db.query(ChatMessage).filter(ChatMessage.roomId == roomId).all()
    return msgs
