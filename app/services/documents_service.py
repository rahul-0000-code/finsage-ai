from fastapi import UploadFile, Depends, Request, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
import os
import uuid

from app.models.document import Document
from app.db.postgres import get_db

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

async def handle_upload(file: UploadFile, user_email: str, db: AsyncSession = Depends(get_db)):
    # storing metadata in Postgres 
    file_id = str(uuid.uuid4())
    file_url = f"/uploads/{file_id}_{file.filename}"
    doc = Document(user_email=user_email, filename=file.filename, file_url=file_url)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return {"msg": f"Uploaded {file.filename}", "file_url": file_url}

async def list_user_documents(user_email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.user_email == user_email))
    docs = result.scalars().all()
    return [
        {"filename": doc.filename, "file_url": doc.file_url, "uploaded_at": doc.uploaded_at}
        for doc in docs
    ]
