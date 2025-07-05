from app.db.postgres import get_db
from app.models.log import ConversationLog
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

# Dummy logs for illustration
user_logs = {}

async def get_current_user():
    # TODO: Implement JWT auth extraction
    return "rahul@gmail.com"

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
