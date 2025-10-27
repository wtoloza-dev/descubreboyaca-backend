"""Remove owner endpoint.

This module provides an endpoint for administrators to remove owners from restaurants.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.dependencies.auth import require_admin_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.restaurant import (
    get_restaurant_owner_service_dependency,
)
from app.domains.restaurants.services import RestaurantOwnerService


router = APIRouter()


@router.delete(
    path="/restaurants/{restaurant_id}/owners/{owner_id}",
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
    service: Annotated[
        RestaurantOwnerService, Depends(get_restaurant_owner_service_dependency)
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
        service: Restaurant owner service (injected)
        current_user: Authenticated user (injected)

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 400 if trying to remove primary owner
        HTTPException: 404 if ownership relationship not found
    """
    await service.remove_owner(
        restaurant_id=str(restaurant_id),
        owner_id=str(owner_id),
    )
