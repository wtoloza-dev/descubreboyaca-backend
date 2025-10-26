"""Google OAuth callback schemas.

This module defines response schemas for Google OAuth callback.
"""

from pydantic import BaseModel

from app.domains.auth.schemas.user import UserSchemaResponse


class GoogleCallbackUserSchemaResponse(BaseModel):
    """Google OAuth callback response.

    Attributes:
        access_token: JWT access token for API authentication
        refresh_token: JWT refresh token for obtaining new access tokens
        token_type: Type of token (always "bearer")
        user: Authenticated user data
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserSchemaResponse
