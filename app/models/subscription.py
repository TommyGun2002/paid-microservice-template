from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SubscriptionStatus(str, Enum):
    FREE = "free"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"
    TRIALING = "trialing"

class SubscriptionPlan(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class PricingTier(BaseModel):
    name: str
    price_id: str
    monthly_price: float
    features: list[str]
    api_call_limit: Optional[int] = None  # None = unlimited
    data_processing_limit: Optional[int] = None  # MB per month

class SubscriptionInfo(BaseModel):
    status: SubscriptionStatus
    plan: SubscriptionPlan
    stripe_subscription_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool = False

class UsageMetrics(BaseModel):
    api_calls_used: int = 0
    api_calls_limit: Optional[int] = None
    data_processing_used: int = 0  # MB
    data_processing_limit: Optional[int] = None  # MB
    current_period_start: datetime
    current_period_end: datetime

class CreateSubscriptionResponse(BaseModel):
    subscription_id: str
    client_secret: Optional[str] = None
    status: str
    message: str

class WebhookEvent(BaseModel):
    event_type: str
    data: Dict[str, Any]
    processed_at: Optional[datetime] = None