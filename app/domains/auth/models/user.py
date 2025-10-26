"""User ORM model.

This module defines the SQLModel for the users table.
"""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    """User ORM model for database persistence.

    This model represents the users table in the database.
    It supports both email/password and OAuth2 authentication.

    Attributes:
        id: Unique user identifier (ULID)
        email: User's email address (unique)
        full_name: User's full name
        hashed_password: Bcrypt hashed password (nullable for OAuth users)
        role: User's role in the system (admin, user, guest)
        is_active: Whether the user account is active
        auth_provider: Authentication provider (email, google, facebook)
        google_id: Google OAuth unique identifier (nullable)
        profile_picture_url: URL to user's profile picture (nullable)
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated (nullable)
    """

    __tablename__ = "users"

    id: str = Field(primary_key=True, max_length=26)
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=255)
    hashed_password: str | None = Field(default=None, max_length=255)
    role: str = Field(default="user", max_length=50)
    is_active: bool = Field(default=True)
    auth_provider: str = Field(default="email", max_length=50)
    google_id: str | None = Field(default=None, max_length=255, index=True)
    profile_picture_url: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = Field(default=None)
