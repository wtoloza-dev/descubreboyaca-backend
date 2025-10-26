"""User domain entities.

This module defines the core User entity and UserData for the authentication domain.
Users can authenticate via email/password or OAuth2 providers (Google, etc.).
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domains.auth.domain.enums.auth_provider import AuthProvider
from app.domains.auth.domain.enums.user_role import UserRole
from app.shared.domain.factories import generate_ulid, generate_utc_now


class UserData(BaseModel):
    """User data without system metadata.

    This represents the core user information without ID and timestamps.
    Used for creating and updating users.

    Attributes:
        email: User's email address (unique identifier)
        full_name: User's full name
        hashed_password: Bcrypt hashed password (None for OAuth users)
        role: User's role in the system
        is_active: Whether the user account is active
        auth_provider: Authentication provider used (email, google, etc.)
        google_id: Google OAuth unique identifier (if using Google auth)
        profile_picture_url: URL to user's profile picture
    """

    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    hashed_password: str | None = Field(default=None, max_length=255)
    role: UserRole = UserRole.USER
    is_active: bool = True
    auth_provider: AuthProvider = AuthProvider.EMAIL
    google_id: str | None = Field(default=None, max_length=255)
    profile_picture_url: str | None = Field(default=None, max_length=500)


class User(UserData):
    """Complete user entity with ID and system metadata.

    This represents the full user entity as stored in the system,
    including auto-generated ID and audit timestamps.

    The ID is automatically generated using ULID for sortable unique identifiers.

    Attributes:
        id: Unique user identifier (ULID)
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=generate_ulid)
    created_at: datetime = Field(default_factory=generate_utc_now)
    updated_at: datetime | None = None
