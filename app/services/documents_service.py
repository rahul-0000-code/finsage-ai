from fastapi import UploadFile

# Dummy storage for illustration
user_docs = {}

async def get_current_user():
    # TODO: Implement JWT auth extraction
    return "demo_user@example.com"

async def handle_upload(file: UploadFile, user_email: str):
    # TODO: Save file to S3/Minio, run OCR, embed, store in Milvus/Neo4j
    user_docs.setdefault(user_email, []).append(file.filename)
    return {"msg": f"Uploaded {file.filename}"}

async def list_user_documents(user_email: str):
    return user_docs.get(user_email, [])
