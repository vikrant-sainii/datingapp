# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---------------------------
# 👤 PROFILE SCHEMAS
# ---------------------------
class ProfileBase(BaseModel):
    name: str
    branch: str
    year: str
    avatar: Optional[str] = None
    personality: Optional[str] = None
    place: Optional[str] = None
    drink: Optional[str] = None
    sports: Optional[str] = None
    mindset: Optional[str] = None
    cgpa: Optional[str] = None


class ProfileCreate(ProfileBase):
    id: str  # provided from frontend


class ProfileOut(ProfileBase):
    id: str

    class Config:
        orm_mode = True



# ---------------------------
# ❤️ HEART SCHEMAS (Updated for JSON MVP)
# ---------------------------
class HeartOut(BaseModel):
    senderId: str
    receiverId: str
    ispending: bool
    sentAt: datetime



# ---------------------------
# 💬 CHAT SCHEMAS
# ---------------------------
class ChatMessageBase(BaseModel):
    text: str


class ChatMessageCreate(ChatMessageBase):
    senderId: str
    receiverId: str


class ChatMessageOut(ChatMessageBase):
    senderId: str
    receiverId: str
    roomId: str
    time: datetime

    class Config:
        orm_mode = True
