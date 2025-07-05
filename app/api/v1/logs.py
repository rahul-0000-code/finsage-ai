from fastapi import APIRouter, Depends
from app.services import logs_service

router = APIRouter()

@router.get("/conversation")
async def get_conversation_logs(user=Depends(logs_service.get_current_user)):
    return await logs_service.get_conversation_history(user)
