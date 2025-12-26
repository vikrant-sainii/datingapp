from fastapi import FastAPI
from database import Base, engine

# Correct router imports
from routes.profiles import router as profiles_router
from routes.hearts import router as hearts_router
from routes.chats import router as chats_router  # optional now
from models import Profile, Heart, ChatMessage, HeartStatus

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(profiles_router, prefix="/profiles", tags=["Profiles"])
app.include_router(hearts_router, prefix="/hearts", tags=["Hearts"])
app.include_router(chats_router, prefix="/chats", tags=["Chats"])  # optional

@app.get("/")
def home():
    return {"status": "API Running 🚀"}
