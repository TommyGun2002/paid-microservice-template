from fastapi import APIRouter

from app.api.v1.endpoints import health, auth, payments, protected, admin

api_router = APIRouter()

# Health check (your existing endpoint)
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Payment and subscription endpoints
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])

# Protected feature endpoints
api_router.include_router(protected.router, prefix="/protected", tags=["protected"])

# Admin endpoints
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])