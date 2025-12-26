from fastapi import FastAPI
from database import Base, engine
from routes import profiles, hearts

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(profiles.router)
app.include_router(hearts.router)

@app.get("/")
def home():
    return {"status": "API is running 🚀"}
