from app.models.goal import UserGoal
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request, HTTPException
from jose import jwt, JWTError
import os

# Dummy advisor logic for illustration
async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid auth token")
    token = auth_header.split(" ")[1]
    SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
    ALGORITHM = "HS256"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def answer_query(query, user_email, db: AsyncSession = Depends(get_db)):
    # 1. Embed query (dummy embedding for now)
    query_embedding = [0.1] * 768
    # 2. Search Milvus for similar docs (dummy result)
    # collection = get_collection("user_docs")
    # results = collection.search(...)
    docs = ["Relevant doc chunk 1", "Relevant doc chunk 2"]
    # 3. Search Neo4j for related tax/investment nodes (dummy result)
    # async with get_neo4j_session() as session:
    #     ...
    graph_context = ["Section 80C", "Capital Gains"]
    # 4. Fetch user profile
    # profile = await fetch_profile(user_email, db)
    # 5. Compose prompt for Gemini (dummy call)
    prompt = f"Q: {query.question}\nDocs: {docs}\nGraph: {graph_context}"
    # TODO: Call Gemini API here
    answer = f"This is a sample answer for: {query.question} (context used: {docs + graph_context})"
    # 6. Save conversation log
    # from app.services.logs_service import save_conversation_log
    # await save_conversation_log(user_email, query.question, answer, db)
    return {"answer": answer, "citations": graph_context}

async def get_suggestions(user_email, db: AsyncSession = Depends(get_db)):
    # Fetch user profile
    # profile = await fetch_profile(user_email, db)
    # TODO: Use profile to generate tips
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
