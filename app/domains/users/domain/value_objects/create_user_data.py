"""Value object for user creation data.

This module defines the value object for user creation before password hashing.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domains.users.domain.enums import UserRole


class CreateUserData(BaseModel):
    """Value object for user creation data (before password hashing).

    This represents the data needed to create a user, with the password
    in plain text (before hashing). This is used as an intermediate value object
    between the request schema and the domain entity.

    Following DDD principles, this value object encapsulates the data needed
    for the create user use case, separating it from the UserData value object
    which contains the hashed password.

    Attributes:
        email: User's email address (unique identifier)
        password: Plain text password (will be hashed by service)
        full_name: User's full name
        role: User's role in the system
        is_active: Whether the user account is active
    """

    model_config = ConfigDict(
        from_attributes=True, validate_assignment=True, frozen=True
    )

    email: EmailStr = Field(description="User's email address")
    password: str = Field(
        min_length=8, max_length=255, description="Plain text password"
    )
    full_name: str = Field(min_length=2, max_length=255, description="User's full name")
    role: UserRole = Field(default=UserRole.USER, description="User's role")
    is_active: bool = Field(default=True, description="Whether account is active")
