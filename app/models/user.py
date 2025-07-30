from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserProfile(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_premium: bool = False
    is_admin: bool = False
    subscription_status: str = "free"
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    api_calls_subscription_item_id: Optional[str] = None
    data_processing_subscription_item_id: Optional[str] = None
    subscription_plan: str = "free"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_premium: Optional[bool] = None
    is_admin: Optional[bool] = None