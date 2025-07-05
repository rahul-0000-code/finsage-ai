from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services import advisor_service

router = APIRouter()

class AdvisorQuery(BaseModel):
    question: str

@router.post("/query")
async def advisor_query(query: AdvisorQuery, user=Depends(advisor_service.get_current_user)):
    return await advisor_service.answer_query(query, user)

@router.get("/suggestions")
async def get_suggestions(user=Depends(advisor_service.get_current_user)):
    return await advisor_service.get_suggestions(user)

@router.post("/goal-plan")
async def save_goal_plan(goals: dict, user=Depends(advisor_service.get_current_user)):
    return await advisor_service.save_goal_plan(user, goals)
