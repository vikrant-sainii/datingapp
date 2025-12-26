# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# -----------------------------
# 🔐 Render / Local DB URL
# Set DATABASE_URL in Render Dashboard
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("❌ DATABASE_URL is missing! Add it in Render Environment Variables.")

# Render uses postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# -----------------------------
# ⚙️ SQLAlchemy Engine Setup
# -----------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -----------------------------
# 📌 Dependency: Get Database Session for Routes
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
