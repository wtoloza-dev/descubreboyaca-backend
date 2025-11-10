"""Create user schemas for admin operations."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domains.users.domain.enums import UserRole


class CreateUserSchemaRequest(BaseModel):
    """Schema for creating a new user (admin operation).

    Attributes:
        email: User's email address (must be unique)
        full_name: User's full name
        password: User's password (plain text, will be hashed)
        role: User role (admin, owner, or user)
        is_active: Whether the user account is active (default: True)
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "newuser@example.com",
                "full_name": "New User",
                "password": "SecurePassword123!",
                "role": "user",
                "is_active": True,
            }
        }
    )

    email: EmailStr = Field(
        description="User's email address (must be unique)",
        examples=["user@example.com"],
    )
    full_name: str = Field(
        min_length=2,
        max_length=255,
        description="User's full name",
        examples=["John Doe"],
    )
    password: str = Field(
        min_length=8,
        max_length=255,
        description="User's password (will be hashed)",
        examples=["SecurePassword123!"],
    )
    role: UserRole = Field(
        default=UserRole.USER,
        description="User role in the system",
        examples=["user", "owner", "admin"],
    )
    is_active: bool = Field(
        default=True,
        description="Whether the user account is active",
    )


class CreateUserSchemaResponse(BaseModel):
    """Schema for created user response.

    Attributes:
        id: User's ULID
        email: User's email address
        full_name: User's full name
        role: User's role
        is_active: Whether the account is active
        created_at: When the user was created
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: str  # Will be serialized from datetime
