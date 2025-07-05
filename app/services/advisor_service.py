from app.models.goal import UserGoal
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

# Dummy advisor logic for illustration
async def get_current_user():
    # TODO: Implement JWT auth extraction
    return "demo_user@example.com"

async def answer_query(query, user_email):
    # TODO: Embed query, search Milvus/Neo4j, call Gemini API
    return {
        "answer": f"This is a sample answer for: {query.question}",
        "citations": ["Section 80C", "Form 16"]
    }

async def get_suggestions(user_email):
    # TODO: Proactive tips based on profile
    return ["Invest in ELSS for tax saving", "Review your insurance coverage"]

async def save_goal_plan(user_email, goals, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserGoal).where(UserGoal.user_email == user_email))
    user_goal = result.scalar_one_or_none()
    if user_goal:
        user_goal.goals = goals
    else:
        user_goal = UserGoal(user_email=user_email, goals=goals)
        db.add(user_goal)
    await db.commit()
    await db.refresh(user_goal)
    return {"msg": "Goals updated"}
