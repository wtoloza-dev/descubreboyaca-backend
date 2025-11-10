"""Create user endpoint (admin only).

This module provides an endpoint for administrators to create new users.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.users.application.services import UserService
from app.domains.users.domain import User
from app.domains.users.domain.value_objects import CreateUserData
from app.domains.users.infrastructure.dependencies import get_user_service_dependency
from app.domains.users.presentation.api.schemas.admin import (
    CreateUserSchemaRequest,
    CreateUserSchemaResponse,
)


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user (Admin only)",
    description="Create a new user with specified role and attributes. "
    "Only administrators can perform this action.",
)
async def handle_create_user(
    request: Annotated[CreateUserSchemaRequest, Body()],
    service: Annotated[UserService, Depends(get_user_service_dependency)],
    admin_user: Annotated[User, Depends(require_admin_dependency)],
) -> CreateUserSchemaResponse:
    """Create a new user.

    **Requiere rol ADMIN**: Solo administradores pueden crear usuarios.

    This endpoint allows administrators to create new users with custom roles,
    including other administrators, owners, and regular users.

    Following DDD patterns, the route handler:
    1. Receives the request schema (API contract)
    2. Converts it to a domain value object (CreateUserData)
    3. Passes the value object to the service for business logic
    4. Returns a properly formatted response

    Args:
        request: User creation request schema (API layer)
        service: User service dependency
        admin_user: Authenticated admin user from dependency

    Returns:
        CreateUserSchemaResponse with created user data

    Raises:
        UserAlreadyExistsException: If email already exists (HTTP 409)
    """
    # Convert request schema to domain value object
    user_data = CreateUserData(**request.model_dump())

    # Pass domain value object to service for entity construction
    user = await service.create(user_data=user_data, created_by=admin_user.id)

    # Build response from entity
    return CreateUserSchemaResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.value,
        is_active=user.is_active,
        created_at=user.created_at.isoformat(),
    )
