from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.services import auth_service

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    phone: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(data: RegisterRequest):
    return await auth_service.register_user(data)

@router.post("/login")
async def login(data: LoginRequest):
    return await auth_service.login_user(data)
