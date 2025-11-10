"""Registration schemas.

This module defines request/response schemas for user registration.
"""

from pydantic import BaseModel, EmailStr, Field

from app.domains.auth.presentation.api.schemas.user import UserSchemaResponse


class RegisterUserSchemaRequest(BaseModel):
    """User registration request schema.

    Attributes:
        email: User's email address
        password: Plain text password (min 8 characters)
        full_name: User's full name
    """

    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["john.doe@example.com"],
    )
    password: str = Field(
        min_length=8,
        max_length=100,
        description="Password must be at least 8 characters long",
        examples=["MySecurePassword123!"],
    )
    full_name: str = Field(
        min_length=2,
        max_length=255,
        description="User's full name",
        examples=["John Doe"],
    )


class RegisterUserSchemaResponse(BaseModel):
    """User registration response schema.

    Attributes:
        user: Created user data
        message: Success message
    """

    user: UserSchemaResponse
    message: str = "User registered successfully"
