from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import redis
from typing import Optional

from app.core.config import settings
from app.api.v1.router import api_router
from app.core.exceptions import CustomException
from app.middleware.rate_limiting import RateLimitMiddleware

# Redis client setup (optional for development)
redis_client: Optional[redis.Redis] = None
try:
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    # Test connection
    redis_client.ping()
    print(f"Connected to Redis at {settings.REDIS_URL}")
except Exception as e:
    print(f"Redis connection failed: {e}. Rate limiting will be disabled.")
    redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"Starting up {settings.PROJECT_NAME}")
    print(f"Version: {settings.VERSION}")
    print(f"Environment: {'Development' if settings.REDIS_URL == 'redis://localhost:6379' else 'Production'}")
    yield
    # Shutdown
    print("Shutting down...")
    if redis_client:
        redis_client.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# Exception handlers
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "error_code": exc.error_code,
            "path": str(request.url.path)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "path": str(request.url.path)
        }
    )

# Middleware (order matters!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Add rate limiting middleware if Redis is available
if redis_client:
    app.add_middleware(RateLimitMiddleware, redis_client=redis_client)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
        "features": [
            "Authentication with Supabase",
            "Payment processing with Stripe", 
            "Rate limiting",
            "Admin functionality",
            "Usage tracking"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "redis_connected": redis_client is not None
    }