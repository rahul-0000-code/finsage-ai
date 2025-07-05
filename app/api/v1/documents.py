from fastapi import APIRouter, UploadFile, File, Depends
from app.services import documents_service

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), user=Depends(documents_service.get_current_user)):
    return await documents_service.handle_upload(file, user)

@router.get("/list")
async def list_documents(user=Depends(documents_service.get_current_user)):
    return await documents_service.list_user_documents(user)
