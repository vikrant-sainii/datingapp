from fastapi import FastAPI
from database import Base, engine
from routes import profiles, hearts, chats

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(profiles.router, prefix="/profiles")
app.include_router(hearts.router, prefix="/hearts")
app.include_router(chats.router, prefix="/chats")

@app.get("/")
def home():
    return {"message": "🚀 Backend running!"}
