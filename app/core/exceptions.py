from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class CustomException(HTTPException):
    """Base custom exception class"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code or "GENERIC_ERROR"

class AuthenticationError(CustomException):
    """Authentication related errors"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTH_ERROR",
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationError(CustomException):
    """Authorization related errors"""
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTH_INSUFFICIENT_PERMISSIONS"
        )

class SubscriptionError(CustomException):
    """Subscription related errors"""
    def __init__(self, detail: str = "Subscription error"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
            error_code="SUBSCRIPTION_ERROR"
        )

class UsageLimitError(CustomException):
    """Usage limit related errors"""
    def __init__(self, detail: str = "Usage limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="USAGE_LIMIT_EXCEEDED"
        )

class PaymentError(CustomException):
    """Payment processing errors"""
    def __init__(self, detail: str = "Payment processing failed"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
            error_code="PAYMENT_ERROR"
        )

class ValidationError(CustomException):
    """Data validation errors"""
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )

class NotFoundError(CustomException):
    """Resource not found errors"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND"
        )

class ServiceUnavailableError(CustomException):
    """Service unavailable errors"""
    def __init__(self, detail: str = "Service temporarily unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            error_code="SERVICE_UNAVAILABLE"
        )