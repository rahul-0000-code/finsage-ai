from app.db.postgres import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import UserProfile

async def get_current_user():
    # TODO: Implement JWT auth extraction
    return "demo_user@example.com"

async def fetch_profile(user_email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserProfile).where(UserProfile.email == user_email))
    profile = result.scalar_one_or_none()
    if not profile:
        return {
            "name": "Demo User",
            "email": user_email,
            "phone": "",
            "income": 0.0,
            "goals": [],
            "risk_profile": "moderate"
        }
    return {
        "name": profile.name,
        "email": profile.email,
        "phone": profile.phone,
        "income": profile.income,
        "goals": profile.goals,
        "risk_profile": profile.risk_profile
    }

async def update_profile(user_email: str, profile, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserProfile).where(UserProfile.email == user_email))
    user = result.scalar_one_or_none()
    if user:
        user.name = profile.name
        user.phone = profile.phone
        user.income = profile.income
        user.goals = profile.goals
        user.risk_profile = profile.risk_profile
    else:
        user = UserProfile(
            name=profile.name,
            email=user_email,
            phone=profile.phone,
            income=profile.income,
            goals=profile.goals,
            risk_profile=profile.risk_profile
        )
        db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"msg": "Profile updated"}
