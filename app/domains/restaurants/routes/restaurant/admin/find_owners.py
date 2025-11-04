"""Find restaurant owners endpoint.

This module provides an endpoint for administrators to find all owners of a restaurant.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.dependencies.auth import require_admin_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.restaurant import (
    get_restaurant_owner_service_dependency,
)
from app.domains.restaurants.schemas.restaurant.admin.find_owners import (
    FindOwnershipsSchemaResponse,
)
from app.domains.restaurants.services import RestaurantOwnerService


router = APIRouter()


@router.get(
    path="/restaurants/{restaurant_id}/owners/",
    status_code=status.HTTP_200_OK,
    summary="Find all owners of a restaurant",
    description="Find all users who have ownership/management rights on a restaurant. Only administrators can access this information.",
)
async def handle_find_owners(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    service: Annotated[
        RestaurantOwnerService, Depends(get_restaurant_owner_service_dependency)
    ],
    current_user: Annotated[User, Depends(require_admin_dependency)],
) -> FindOwnershipsSchemaResponse:
    """Find all owners/managers/staff of a restaurant.

    **Requiere autenticación**: Solo administradores (ADMIN) pueden ver owners.

    This endpoint returns all users who have been assigned to manage this restaurant,
    including their roles (owner, manager, staff) and whether they are the primary owner.

    Args:
        restaurant_id: ULID of the restaurant
        service: Restaurant owner service (injected)
        current_user: Authenticated user (injected)

    Returns:
        FindOwnershipsSchemaResponse: List of owners with their roles

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 404 if restaurant not found
    """
    owners = await service.get_owners_by_restaurant(str(restaurant_id))

    return FindOwnershipsSchemaResponse(
        restaurant_id=str(restaurant_id),
        owners=owners,
        total=len(owners),
    )
