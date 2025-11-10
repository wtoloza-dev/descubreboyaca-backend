"""Token refresh schemas.

This module defines request/response schemas for token refresh operations.
"""

from pydantic import BaseModel


class RefreshUserSchemaRequest(BaseModel):
    """Refresh token request schema.

    Attributes:
        refresh_token: JWT refresh token
    """

    refresh_token: str


class RefreshUserSchemaResponse(BaseModel):
    """Token response schema.

    Attributes:
        access_token: JWT access token for API authentication
        token_type: Type of token (always "bearer")
    """

    access_token: str
    token_type: str = "bearer"
