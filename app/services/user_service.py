from app.db.postgres import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Dummy user profile for illustration
user_profiles = {}

async def get_current_user():
    # TODO: Implement JWT auth extraction
    return "demo_user@example.com"

async def fetch_profile(user_email: str):
    return user_profiles.get(user_email, {
        "name": "Demo User",
        "email": user_email,
        "phone": "",
        "income": 0.0,
        "goals": [],
        "risk_profile": "moderate"
    })

async def update_profile(user_email: str, profile):
    user_profiles[user_email] = profile.dict()
    return {"msg": "Profile updated"}
