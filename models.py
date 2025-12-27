from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# ---------- PROFILE TABLE ----------
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    branch = Column(String)
    year = Column(String)
    avatar = Column(String)

    personality = Column(String)
    place = Column(String)
    drink = Column(String)
    sports = Column(String)
    mindset = Column(String)
    cgpa = Column(String)

    # relationships for future
    sent_hearts = relationship("Heart", foreign_keys="Heart.senderId")
    received_hearts = relationship("Heart", foreign_keys="Heart.receiverId")


# ---------- HEART TABLE (NOT USED YET, FOR FUTURE SCALE) ----------
class Heart(Base):
    __tablename__ = "hearts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    senderId = Column(String, ForeignKey("profiles.id"), nullable=False)
    receiverId = Column(String, ForeignKey("profiles.id"), nullable=False)
    ispending = Column(Boolean, default=True)
    sentAt = Column(DateTime, default=lambda: datetime.utcnow())


# ---------- CHAT TABLE (Future real chat) ----------
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    roomId = Column(String, index=True)
    senderId = Column(String, ForeignKey("profiles.id"))
    receiverId = Column(String, ForeignKey("profiles.id"))
    text = Column(Text, nullable=False)
    time = Column(DateTime, default=lambda: datetime.utcnow())


# ---------- JSON STORE IN DATABASE FOR HEART/MUTUAL MVP ----------
class AppState(Base):
    __tablename__ = "app_state"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hearts = Column(JSON, nullable=False, default=lambda: {
        "sent": {},
        "received": {},
        "mutual": {}
    })
