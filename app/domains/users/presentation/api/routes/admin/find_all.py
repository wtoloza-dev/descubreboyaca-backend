"""Find all users endpoint (admin only).

This module provides an endpoint for administrators to list all users.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.users.application.services import UserService
from app.domains.users.domain import User
from app.domains.users.infrastructure.dependencies import get_user_service_dependency
from app.domains.users.presentation.api.schemas.admin import (
    FindAllUsersSchemaResponse,
    UserSchemaItem,
)
from app.shared.dependencies.pagination import get_pagination_dependency
from app.shared.domain import Pagination
from app.shared.schemas.pagination import PaginationSchemaData


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List all users (Admin only)",
    description="Retrieve a paginated list of all users in the system. "
    "Only administrators can perform this action.",
)
async def handle_find_all_users(
    service: Annotated[UserService, Depends(get_user_service_dependency)],
    admin_user: Annotated[User, Depends(require_admin_dependency)],
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
) -> FindAllUsersSchemaResponse:
    """Find all users with pagination.

    **Requiere rol ADMIN**: Solo administradores pueden listar usuarios.

    This endpoint returns all users in the system with pagination support.
    Useful for user management, auditing, and administrative tasks.

    Args:
        service: User service dependency
        admin_user: Authenticated admin user from dependency
        pagination: Pagination parameters (offset, limit)

    Returns:
        FindAllUsersSchemaResponse with list of users and pagination metadata
    """
    users, total = await service.find_all(
        offset=pagination.offset, limit=pagination.limit
    )

    return FindAllUsersSchemaResponse(
        data=[
            UserSchemaItem(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                role=user.role.value,
                is_active=user.is_active,
                auth_provider=user.auth_provider.value,
                created_at=user.created_at.isoformat(),
            )
            for user in users
        ],
        pagination=PaginationSchemaData(
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        ),
    )
