"""User schemas.

This module defines shared user schemas used across auth endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchemaResponse(BaseModel):
    """User response schema.

    This schema is used to return user data in API responses.
    Sensitive information like passwords are excluded.

    Attributes:
        id: User's unique identifier (ULID)
        email: User's email address
        full_name: User's full name
        role: User's role in the system
        is_active: Whether the user account is active
        auth_provider: Authentication provider used
        profile_picture_url: URL to user's profile picture
        created_at: Timestamp when user was created
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    auth_provider: str
    profile_picture_url: str | None = None
    created_at: datetime
