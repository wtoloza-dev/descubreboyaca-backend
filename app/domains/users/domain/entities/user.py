"""User domain entities following DDD principles.

This module defines the core User entity and UserData for the authentication domain.
Users can authenticate via email/password or OAuth2 providers (Google, etc.).
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domains.users.domain.enums.auth_provider import AuthProvider
from app.domains.users.domain.enums.user_role import UserRole
from app.shared.domain.entities import Audit


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

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    hashed_password: str | None = Field(default=None, max_length=255)
    role: UserRole = UserRole.USER
    is_active: bool = True
    auth_provider: AuthProvider = AuthProvider.EMAIL
    google_id: str | None = Field(default=None, max_length=255)
    profile_picture_url: str | None = Field(default=None, max_length=500)


class User(UserData, Audit):
    """Complete user entity with ID and full audit trail.

    This represents the full user entity as stored in the system,
    including auto-generated ID and complete audit tracking.

    Following DDD principles, the entity generates its own identity (ULID)
    and audit fields through inheritance from Audit.

    Uses full Audit (with created_by/updated_by) to support future scenarios:
    - Admin-created user accounts
    - Support staff modifications
    - System migrations and bulk operations
    - Compliance and security audit requirements

    For self-registration, created_by can be set to the user's own ID after creation,
    or left as None to indicate self-service registration.

    Attributes:
        id: Unique user identifier (ULID, inherited from Audit)
        created_at: Timestamp when user was created (inherited from Audit)
        updated_at: Timestamp when user was last updated (inherited from Audit)
        created_by: User/Admin who created this account (inherited from Audit, nullable for self-registration)
        updated_by: User/Admin who last updated this account (inherited from Audit, nullable for self-updates)
    """
