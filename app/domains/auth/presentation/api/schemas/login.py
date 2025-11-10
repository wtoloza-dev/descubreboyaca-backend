"""Login schemas.

This module defines request/response schemas for user login.
"""

from pydantic import BaseModel, EmailStr

from app.domains.auth.presentation.api.schemas.user import UserSchemaResponse


class LoginUserSchemaRequest(BaseModel):
    """User login request schema.

    Attributes:
        email: User's email address
        password: Plain text password
    """

    email: EmailStr
    password: str


class LoginUserSchemaResponse(BaseModel):
    """User login response schema.

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
