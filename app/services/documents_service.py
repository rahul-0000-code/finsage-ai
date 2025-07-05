from fastapi import UploadFile, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.models.document import Document

# Dummy storage for illustration
user_docs = {}

async def get_current_user():
    # TODO: Implement JWT auth extraction
    return "demo_user@example.com"

async def handle_upload(file: UploadFile, user_email: str, db: AsyncSession = Depends(get_db)):
    # TODO: Save file to S3/Minio, run OCR, embed, store in Milvus/Neo4j
    file_id = str(uuid.uuid4())
    file_url = f"s3://bucket/{file_id}_{file.filename}"
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
