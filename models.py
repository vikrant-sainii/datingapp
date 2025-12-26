from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum, datetime

class HeartStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    branch = Column(String)
    year = Column(String)
    avatar = Column(String)

class Heart(Base):
    __tablename__ = "hearts"
    id = Column(Integer, primary_key=True, index=True)
    senderId = Column(String, ForeignKey("profiles.id"))
    receiverId = Column(String, ForeignKey("profiles.id"))
    status = Column(Enum(HeartStatus), default=HeartStatus.pending)
    sentAt = Column(DateTime, default=datetime.datetime.utcnow)
