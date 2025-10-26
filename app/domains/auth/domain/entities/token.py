"""Token domain entities.

This module defines JWT token entities for authentication.
"""

from datetime import datetime

from pydantic import BaseModel


class TokenData(BaseModel):
    """JWT token data.

    Contains the access token and optional refresh token.

    Attributes:
        access_token: JWT access token for API authentication
        refresh_token: JWT refresh token for obtaining new access tokens
        token_type: Type of token (always "bearer" for JWT)
    """

    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class Token(TokenData):
    """Complete token entity with metadata.

    Extends TokenData with additional metadata about token expiration.

    Attributes:
        expires_at: Timestamp when the access token expires
    """

    expires_at: datetime
