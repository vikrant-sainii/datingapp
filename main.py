from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes.profiles import router as profiles_router
from routes.hearts import router as hearts_router
from routes.chats import router as chats_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dating App Backend")

# -----------------------
# 🔧 CORS CONFIG (FIX)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # allow all clients for now (Flutter/mobile/web)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# ROUTES
# -----------------------
app.include_router(profiles_router)
app.include_router(hearts_router)
app.include_router(chats_router)

@app.get("/")
def home():
    return {"message": "🚀 Backend Running"}
