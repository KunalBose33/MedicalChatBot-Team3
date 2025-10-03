from fastapi import APIRouter

router = APIRouter()

@router.post("/send")
def send_message():
    return {"message": "Send chat endpoint placeholder"}

@router.get("/history")
def get_chat_history():
    return {"messages": []}
