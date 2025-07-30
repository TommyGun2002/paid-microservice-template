from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from pydantic import BaseModel, EmailStr

from app.core.deps import get_current_active_user
from app.services.supabase_service import supabase_service

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class ProfileUpdate(BaseModel):
    full_name: str

@router.post("/signup")
async def signup(signup_data: SignupRequest):
    """Register a new user"""
    return {
        "message": "Signup endpoint - integrate with your frontend auth",
        "note": "User signup handled by Supabase Auth on frontend"
    }

@router.post("/login")
async def login(login_data: LoginRequest):
    """Login user"""
    return {
        "message": "Login endpoint - integrate with your frontend auth", 
        "note": "User login handled by Supabase Auth on frontend"
    }

@router.get("/profile")
async def get_profile(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """Get current user profile"""
    return {
        "user_id": current_user["id"],
        "email": current_user["email"],
        "profile": current_user["profile"],
        "subscription_status": current_user["profile"].get("subscription_status", "free")
    }

@router.put("/profile")
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """Update user profile"""
    return {"message": "Profile update endpoint - implement based on your needs"}