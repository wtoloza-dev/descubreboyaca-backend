"""User model for database persistence.

This module defines the SQLModel for the users table.
"""

from sqlmodel import Field, SQLModel

from app.shared.models import AuditMixin


class UserModel(AuditMixin, SQLModel, table=True):
    """User model for database persistence.

    This model represents the users table in the database.
    It supports both email/password and OAuth2 authentication.

    Note: Following DDD principles, the ID and timestamps must be provided
    by the User domain entity. This model only persists the data.

    Attributes:
        id: Unique user identifier (ULID) - inherited from AuditMixin
        email: User's email address (unique)
        full_name: User's full name
        hashed_password: Bcrypt hashed password (nullable for OAuth users)
        role: User's role in the system (admin, user, guest)
        is_active: Whether the user account is active
        auth_provider: Authentication provider (email, google, facebook)
        google_id: Google OAuth unique identifier (nullable)
        profile_picture_url: URL to user's profile picture (nullable)
        created_at: Timestamp when user was created - inherited from AuditMixin
        updated_at: Timestamp when user was last updated - inherited from AuditMixin
        created_by: ULID of user who created this account - inherited from AuditMixin
        updated_by: ULID of user who last updated this account - inherited from AuditMixin
    """

    __tablename__ = "users"

    # User data
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User's email address",
    )
    full_name: str = Field(
        max_length=255,
        description="User's full name",
    )
    hashed_password: str | None = Field(
        default=None,
        max_length=255,
        description="Bcrypt hashed password (nullable for OAuth users)",
    )
    role: str = Field(
        default="user",
        max_length=50,
        description="User's role in the system",
    )
    is_active: bool = Field(
        default=True,
        description="Whether the user account is active",
    )
    auth_provider: str = Field(
        default="email",
        max_length=50,
        description="Authentication provider (email, google, facebook)",
    )
    google_id: str | None = Field(
        default=None,
        max_length=255,
        index=True,
        description="Google OAuth unique identifier",
    )
    profile_picture_url: str | None = Field(
        default=None,
        max_length=500,
        description="URL to user's profile picture",
    )
