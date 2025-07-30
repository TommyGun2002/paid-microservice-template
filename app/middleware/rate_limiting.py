import time
import redis
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from typing import Optional

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client: Optional[redis.Redis] = None):
        super().__init__(app)
        self.redis_client = redis_client
        self.rate_limit = settings.RATE_LIMIT_PER_MINUTE
        
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting if Redis is not available
        if not self.redis_client:
            return await call_next(request)
        
        # Get client IP
        client_ip = self.get_client_ip(request)
        
        # Create rate limit key
        rate_limit_key = f"rate_limit:{client_ip}"
        current_time = int(time.time())
        window_start = current_time - 60  # 1 minute window
        
        try:
            # Clean old entries
            self.redis_client.zremrangebyscore(rate_limit_key, 0, window_start)
            
            # Count current requests
            current_requests = self.redis_client.zcard(rate_limit_key)
            
            # Check if rate limit exceeded
            if current_requests >= self.rate_limit:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "Rate limit exceeded",
                        "detail": f"Maximum {self.rate_limit} requests per minute allowed",
                        "retry_after": 60
                    },
                    headers={"Retry-After": "60"}
                )
            
            # Add current request
            self.redis_client.zadd(rate_limit_key, {str(current_time): current_time})
            self.redis_client.expire(rate_limit_key, 60)
            
        except Exception as e:
            # If Redis fails, continue without rate limiting
            print(f"Rate limiting error: {e}")
        
        response = await call_next(request)
        
        # Add rate limit headers
        if self.redis_client:
            try:
                remaining = max(0, self.rate_limit - current_requests - 1)
                response.headers["X-RateLimit-Limit"] = str(self.rate_limit)
                response.headers["X-RateLimit-Remaining"] = str(remaining)
                response.headers["X-RateLimit-Reset"] = str(current_time + 60)
            except:
                pass
        
        return response
    
    def get_client_ip(self, request: Request) -> str:
        """Get client IP address from request"""
        # Check for forwarded IP first (for load balancers/proxies)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check for real IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to client host
        return request.client.host if request.client else "unknown"