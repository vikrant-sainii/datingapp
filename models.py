# models.py
from sqlalchemy import (
    Column, String, Integer, DateTime, ForeignKey, Enum, Text
)
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime


# ---------- ENUMS ----------
class HeartStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"


# ---------- PROFILE MODEL ----------
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, index=True)  # same as app userId
    name = Column(String, nullable=False)
    branch = Column(String, nullable=True)
    year = Column(String, nullable=True)
    avatar = Column(String, nullable=True)  # image URL/path

    # ✔ reverse relations (optional)
    sent_hearts = relationship("Heart", foreign_keys="Heart.senderId", backref="sender_profile")
    received_hearts = relationship("Heart", foreign_keys="Heart.receiverId", backref="receiver_profile")


# ---------- HEART MODEL ----------
class Heart(Base):
    __tablename__ = "hearts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    senderId = Column(String, ForeignKey("profiles.id"))
    receiverId = Column(String, ForeignKey("profiles.id"))
    status = Column(Enum(HeartStatus), default=HeartStatus.pending)
    sentAt = Column(DateTime, default=datetime.timezone.utc)


# ---------- MUTUAL MATCH MODEL ----------
# When userA accepts userB → both get a row here.
class Mutual(Base):
    __tablename__ = "mutuals"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userA = Column(String, ForeignKey("profiles.id"))
    userB = Column(String, ForeignKey("profiles.id"))
    matchedAt = Column(DateTime, default=datetime.timezone.utc)


# ---------- CHAT MODEL ----------
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    roomId = Column(String, index=True)  # generated as sorted: "userA_userB"
    senderId = Column(String, ForeignKey("profiles.id"))
    receiverId = Column(String, ForeignKey("profiles.id"))
    text = Column(Text, nullable=False)
    time = Column(DateTime, default=datetime.timezone.utc)
