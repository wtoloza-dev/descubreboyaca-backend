"""Remove owner endpoint.

This module provides an endpoint for administrators to remove owners from restaurants.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    RemoveOwnerUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_remove_owner_use_case_dependency,
)
from app.domains.users.domain import User


router = APIRouter()


@router.delete(
    path="/restaurants/{restaurant_id}/owners/{owner_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove an owner from a restaurant",
    description="Remove a user's ownership/management rights from a restaurant. Only administrators can perform this action.",
)
async def handle_remove_owner(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    owner_id: Annotated[
        ULID,
        Path(
            description="ULID of the owner",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    use_case: Annotated[
        RemoveOwnerUseCase, Depends(get_remove_owner_use_case_dependency)
    ],
    current_user: Annotated[User, Depends(require_admin_dependency)],
) -> None:
    """Remove an owner/manager/staff from a restaurant.

    **Requiere autenticación**: Solo administradores (ADMIN) pueden remover owners.

    This endpoint removes a user's management rights from a restaurant.
    Note: Cannot remove the primary owner without transferring ownership first.

    Args:
        restaurant_id: ULID of the restaurant
        owner_id: ULID of the owner to remove
        use_case: Remove owner use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 400 if trying to remove primary owner
        HTTPException: 404 if ownership relationship not found
    """
    await use_case.execute(
        restaurant_id=str(restaurant_id),
        owner_id=str(owner_id),
    )
