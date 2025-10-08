"""
Common schemas used across multiple endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ErrorResponse(BaseModel):
    """
    Standard error response schema.
    
    Attributes:
        error: Error message
        detail: Optional detailed error information
        status_code: HTTP status code
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")

