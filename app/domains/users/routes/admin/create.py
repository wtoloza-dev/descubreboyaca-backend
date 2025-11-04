"""Create user endpoint (admin only).

This module provides an endpoint for administrators to create new users.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.auth.dependencies.auth import require_admin_dependency
from app.domains.auth.domain import User
from app.domains.users.dependencies import get_user_service_dependency
from app.domains.users.schemas.admin import (
    CreateUserSchemaRequest,
    CreateUserSchemaResponse,
)
from app.domains.users.services import UserService


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

    Args:
        request: User creation request with email, password, full_name, role, is_active
        service: User service dependency
        admin_user: Authenticated admin user from dependency

    Returns:
        CreateUserSchemaResponse with created user data

    Raises:
        UserAlreadyExistsException: If email already exists (HTTP 409)
    """
    user = await service.create(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        role=request.role,
        is_active=request.is_active,
        created_by=admin_user.id,
    )

    return CreateUserSchemaResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.value,
        is_active=user.is_active,
        created_at=user.created_at.isoformat(),
    )
