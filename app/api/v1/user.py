from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services import user_service

router = APIRouter()

class UserProfile(BaseModel):
    name: str
    email: str
    phone: str
    income: float
    goals: list[str]
    risk_profile: str

@router.get("/profile", response_model=UserProfile)
async def get_profile(user=Depends(user_service.get_current_user)):
    return await user_service.fetch_profile(user)

@router.put("/profile")
async def update_profile(profile: UserProfile, user=Depends(user_service.get_current_user)):
    return await user_service.update_profile(user, profile)
