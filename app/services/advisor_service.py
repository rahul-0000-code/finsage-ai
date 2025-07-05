from app.models.goal import UserGoal
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request, HTTPException
from jose import jwt, JWTError
import os
from app.db.milvus import get_collection
from app.db.neo4j import get_neo4j_session
from app.services.user_service import fetch_profile
from app.services.logs_service import save_conversation_log
from sentence_transformers import SentenceTransformer
import requests

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

# Load embedding model once (singleton)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://gemini.googleapis.com/v1/generate")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "dummy-key")

async def answer_query(query, user_email, db: AsyncSession = Depends(get_db)):
    # 1. Embed query using SentenceTransformer
    query_embedding = embedding_model.encode(query.question).tolist()
    # 2. Search Milvus for similar docs
    try:
        collection = get_collection("user_docs")
        milvus_results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=5,
            expr=f"user_email == '{user_email}'"
        )
        docs = [hit.entity.get('text') for hit in milvus_results[0]]
    except Exception:
        docs = []
    # 3. Search Neo4j for related tax/investment nodes
    graph_context = []
    try:
        async with get_neo4j_session() as session:
            cypher = "MATCH (n:TaxSection)-[:RELATED_TO]->(m) RETURN n.name as section, m.name as related LIMIT 5"
            result = await session.run(cypher)
            graph_context = [record["section"] + ": " + record["related"] for record in await result.to_list()]
    except Exception:
        graph_context = []
    # 4. Fetch user profile
    profile = await fetch_profile(user_email, db)
    # 5. Compose prompt for Gemini
    prompt = f"Q: {query.question}\nDocs: {docs}\nGraph: {graph_context}\nProfile: {profile}"
    # 6. Call Gemini API (stub)
    try:
        response = requests.post(
            GEMINI_API_URL,
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
            json={"prompt": prompt}
        )
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer from Gemini.")
        else:
            answer = f"Gemini API error: {response.status_code}"
    except Exception as e:
        answer = f"Gemini API call failed: {e}"
    # 7. Save conversation log
    await save_conversation_log(user_email, query.question, answer, db)
    return {"answer": answer, "citations": docs + graph_context}

async def get_suggestions(user_email, db: AsyncSession = Depends(get_db)):
    profile = await fetch_profile(user_email, db)
    tips = []
    if profile.get("income", 0) < 500000:
        tips.append("Consider investing in PPF or ELSS for tax saving.")
    if profile.get("goals") and "retirement" in profile["goals"]:
        tips.append("Start a SIP in a retirement-focused mutual fund.")
    if profile.get("risk_profile") == "aggressive":
        tips.append("Explore equity mutual funds for higher returns.")
    if not tips:
        tips = ["Invest in ELSS for tax saving", "Review your insurance coverage"]
    return tips

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
