from fastapi import APIRouter, Depends
from typing import Dict, Any, List

from app.core.deps import get_admin_user
from app.services.supabase_service import supabase_service

router = APIRouter()

@router.get("/users")
async def list_users(
    admin_user: Dict[str, Any] = Depends(get_admin_user)
):
    """List all users (admin only)"""
    return {
        "message": "Admin endpoint - list all users",
        "note": "Implement user listing from Supabase",
        "admin": admin_user["profile"].get("full_name", "Admin")
    }

@router.get("/subscriptions")
async def subscription_overview(
    admin_user: Dict[str, Any] = Depends(get_admin_user)
):
    """Get subscription overview (admin only)"""
    return {
        "message": "Admin endpoint - subscription analytics",
        "note": "Implement subscription metrics and analytics"
    }

@router.post("/users/{user_id}/subscription")
async def modify_user_subscription(
    user_id: str,
    admin_user: Dict[str, Any] = Depends(get_admin_user)
):
    """Modify user subscription (admin only)"""
    return {
        "message": f"Admin endpoint - modify subscription for user {user_id}",
        "note": "Implement subscription management for customer support"
    }