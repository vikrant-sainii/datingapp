from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class ProfileSchema(BaseModel):
    id: str
    name: str
    branch: str
    year: str
    avatar: str

class HeartStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"

class HeartSchema(BaseModel):
    senderId: str
    receiverId: str
    status: HeartStatus = HeartStatus.pending


class ChatMessageCreate(BaseModel):
    senderId: str
    receiverId: str
    text: str

class ChatMessageOut(ChatMessageCreate):
    time: datetime = datetime.now()
    roomId: str | None = None

    class Config:
        orm_mode = True

