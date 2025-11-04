"""Find all users schemas for admin operations."""

from pydantic import BaseModel, ConfigDict

from app.shared.schemas.pagination import PaginationSchemaData


class UserSchemaItem(BaseModel):
    """Schema for a user item in list response.

    Attributes:
        id: User's ULID
        email: User's email address
        full_name: User's full name
        role: User's role
        is_active: Whether the account is active
        auth_provider: Authentication provider (email or google)
        created_at: When the user was created
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    auth_provider: str
    created_at: str  # Will be serialized from datetime


class FindAllUsersSchemaResponse(BaseModel):
    """Schema for find all users response with pagination.

    Attributes:
        data: List of users
        pagination: Pagination metadata
    """

    model_config = ConfigDict(from_attributes=True)

    data: list[UserSchemaItem]
    pagination: PaginationSchemaData
