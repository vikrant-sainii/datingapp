from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def chat_home():
    return {"message": "chats endpoint working!"}
