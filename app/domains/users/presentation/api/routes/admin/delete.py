"""Delete user endpoint (admin only).

This module provides an endpoint for administrators to delete users.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.users.application.services import UserService
from app.domains.users.domain import User
from app.domains.users.infrastructure.dependencies import get_user_service_dependency
from app.domains.users.presentation.api.schemas.admin import DeleteUserSchemaRequest


router = APIRouter()


@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user (Admin only)",
    description="Soft-delete a user and archive their data for audit purposes. "
    "The user will be removed from active tables but preserved in the archive. "
    "Only administrators can perform this action.",
)
async def handle_delete_user(
    user_id: Annotated[str, Path(description="ULID of the user to delete")],
    request: Annotated[DeleteUserSchemaRequest, Body()],
    service: Annotated[UserService, Depends(get_user_service_dependency)],
    admin_user: Annotated[User, Depends(require_admin_dependency)],
) -> None:
    """Delete a user with archiving.

    **Requiere rol ADMIN**: Solo administradores pueden eliminar usuarios.

    This endpoint performs a soft delete with archiving:
    1. Saves user data to the archive table for audit trail
    2. Removes user from the active users table

    This ensures data preservation for compliance and auditing while
    removing the user from active operations.

    Args:
        user_id: ULID of the user to delete
        request: Delete request with optional note
        service: User service dependency
        admin_user: Authenticated admin user from dependency

    Raises:
        UserNotFoundException: If user doesn't exist (HTTP 404)
    """
    await service.delete(
        user_id=user_id,
        deleted_by=admin_user.id,
        note=request.note,
    )
