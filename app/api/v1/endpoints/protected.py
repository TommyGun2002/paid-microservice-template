from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.core.deps import get_current_active_user, get_premium_user
from app.models.response import MessageResponse

router = APIRouter()

@router.get("/free-feature")
async def free_feature(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """Free feature available to all authenticated users"""
    return {
        "message": f"Hello {current_user['profile'].get('full_name', 'User')}!",
        "feature": "This is a free feature available to all users",
        "user_id": current_user["id"]
    }

@router.get("/premium-feature")
async def premium_feature(
    current_user: Dict[str, Any] = Depends(get_premium_user)
):
    """Premium feature requiring premium subscription"""
    return {
        "message": f"Welcome Premium User {current_user['profile'].get('full_name', 'User')}!",
        "feature": "This is an exclusive premium feature",
        "premium_data": "Advanced analytics, unlimited API calls, priority support"
    }

@router.post("/usage-tracked-feature")
async def usage_tracked_feature(
    data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """Feature that tracks usage for metered billing"""
    
    # Process the request
    result = {"processed": True, "input_data": data}
    
    # Track usage (placeholder for now)
    usage_info = {
        "user_id": current_user["id"],
        "feature": "usage_tracked_feature", 
        "units_consumed": 1,
        "note": "Usage tracking will be implemented with Stripe metered billing"
    }
    
    return {
        "result": result,
        "usage": usage_info
    }