from pydantic import BaseModel
from enum import Enum
from typing import Optional

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
