import stripe
from app.core.config import settings
from typing import Dict, Any

# Only initialize if we have Stripe keys
if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    def __init__(self):
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    
    async def create_customer(self, email: str, name: str, user_id: str) -> Dict[str, Any]:
        """Create a new Stripe customer"""
        if not settings.STRIPE_SECRET_KEY:
            raise ValueError("Stripe not configured")
        
        customer = stripe.Customer.create(
            email=email,
            name=name,
            metadata={"user_id": user_id}
        )
        return customer

stripe_service = StripeService()