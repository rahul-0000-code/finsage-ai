from fastapi import APIRouter, Depends
from app.services import admin_service

router = APIRouter()

@router.get("/stats")
async def get_admin_stats(user=Depends(admin_service.get_current_admin)):
    return await admin_service.get_stats(user)
