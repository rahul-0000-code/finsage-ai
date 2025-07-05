from app.db.postgres import get_db
from app.models.log import ConversationLog
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request, HTTPException
from jose import jwt, JWTError
import os

# Dummy logs for illustration
user_logs = {}

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

async def get_conversation_history(user_email, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ConversationLog).where(ConversationLog.user_email == user_email))
    logs = result.scalars().all()
    return [
        {"question": log.question, "answer": log.answer, "created_at": log.created_at}
        for log in logs
    ]

async def save_conversation_log(user_email, question, answer, db: AsyncSession):
    log = ConversationLog(user_email=user_email, question=question, answer=answer)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log
