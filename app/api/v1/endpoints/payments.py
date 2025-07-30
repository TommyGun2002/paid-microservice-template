from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any
from pydantic import BaseModel

from app.core.deps import get_current_active_user
from app.services.stripe_service import stripe_service
from app.services.supabase_service import supabase_service
from app.models.response import MessageResponse

router = APIRouter()

class CreateSubscriptionRequest(BaseModel):
    price_id: str

@router.post("/create-subscription")
async def create_subscription(
    request: CreateSubscriptionRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """Create a new subscription for the user"""
    try:
        profile = current_user["profile"]
        
        customer = await stripe_service.create_customer(
            email=current_user["email"],
            name=profile.get("full_name", ""),
            user_id=current_user["id"]
        )
        
        return {
            "customer_id": customer["id"],
            "message": "Customer created - implement full subscription flow"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """Cancel user's subscription"""
    return MessageResponse(message="Subscription cancellation endpoint")

@router.get("/subscription-status")
async def get_subscription_status(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """Get user's current subscription status"""
    profile = current_user["profile"]
    return {
        "status": profile.get("subscription_status", "free"),
        "is_premium": profile.get("is_premium", False),
        "stripe_customer_id": profile.get("stripe_customer_id")
    }

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    try:
        payload = await request.body()
        signature = request.headers.get("stripe-signature")
        
        return JSONResponse(content={"status": "webhook received"})
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))