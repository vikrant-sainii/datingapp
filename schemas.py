# schemas.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

# ---------------------------
# ❤️ Heart Status Enum
# ---------------------------
class HeartStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"

# ---------------------------
# 👤 PROFILE SCHEMAS
# ---------------------------
class ProfileBase(BaseModel):
    name: str
    branch: str
    year: str
    avatar: Optional[str] = None
    personality: Optional[str] = ""
    place: Optional[str] = ""
    drink: Optional[str] = ""
    sports: Optional[str] = ""
    mindset: Optional[str] = ""
    cgpa: Optional[str] = ""


class ProfileCreate(ProfileBase):
    id: str   # we assign ID from frontend for now (later from auth system)


class ProfileOut(ProfileBase):
    id: str

    class Config:
        orm_mode = True  # <- VERY IMPORTANT


# ---------------------------
# ❤️ HEART SCHEMAS
# ---------------------------
class HeartBase(BaseModel):
    senderId: str
    receiverId: str
    status: HeartStatus = HeartStatus.pending


class HeartCreate(HeartBase):
    pass


class HeartOut(HeartBase):
    id: int
    sentAt: datetime

    class Config:
        orm_mode = True


# ---------------------------
# 💬 CHAT SCHEMAS
# ---------------------------
class ChatMessageBase(BaseModel):
    text: str


class ChatMessageCreate(ChatMessageBase):
    senderId: str
    receiverId: str
    roomId: str


class ChatMessageOut(ChatMessageBase):
    senderId: str
    receiverId: str
    roomId: str
    time: datetime

    class Config:
        orm_mode = True
