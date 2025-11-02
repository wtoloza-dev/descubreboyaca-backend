"""Token domain value objects.

This module defines JWT token value objects for authentication responses.
Tokens are ephemeral response objects, not persisted entities.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TokenData(BaseModel):
    """JWT token data value object.

    Immutable value object containing JWT authentication tokens.
    This is a value object because tokens are not persisted
    and have no database identity - they are ephemeral response data.

    Attributes:
        access_token: JWT access token for API authentication
        refresh_token: JWT refresh token for obtaining new access tokens
        token_type: Type of token (always "bearer" for JWT)
    """

    model_config = ConfigDict(frozen=True)

    access_token: str = Field(description="JWT access token")
    refresh_token: str | None = Field(
        default=None, description="JWT refresh token for token renewal"
    )
    token_type: str = Field(default="bearer", description="Token type (bearer)")


class Token(TokenData):
    """Complete token value object with metadata.

    Immutable value object extending TokenData with token expiration information.
    This is used for authentication responses that include expiration metadata.

    Attributes:
        expires_at: Timestamp when the access token expires
    """

    model_config = ConfigDict(frozen=True)

    expires_at: datetime = Field(description="Token expiration timestamp")
