"""List restaurant owners endpoint.

This module provides an endpoint for administrators to list all owners of a restaurant.
"""

from fastapi import APIRouter, Depends, status

from app.domains.auth.dependencies.auth import require_admin_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.sql import (
    get_restaurant_owner_service_dependency,
)
from app.domains.restaurants.schemas.restaurant.ownership import (
    OwnershipListSchemaResponse,
)
from app.domains.restaurants.services import RestaurantOwnerService


router = APIRouter()


@router.get(
    path="/restaurants/{restaurant_id}/owners",
    status_code=status.HTTP_200_OK,
    summary="List all owners of a restaurant",
    description="Get a list of all users who have ownership/management rights on a restaurant. Only administrators can access this information.",
)
async def handle_list_owners(
    restaurant_id: str,
    service: RestaurantOwnerService = Depends(get_restaurant_owner_service_dependency),
    current_user: User = Depends(require_admin_dependency),
) -> OwnershipListSchemaResponse:
    """List all owners/managers/staff of a restaurant.

    **Requiere autenticación**: Solo administradores (ADMIN) pueden ver owners.

    This endpoint returns all users who have been assigned to manage this restaurant,
    including their roles (owner, manager, staff) and whether they are the primary owner.

    Args:
        restaurant_id: ULID of the restaurant
        service: Restaurant owner service (injected)
        current_user: Authenticated user (injected)

    Returns:
        OwnershipListSchemaResponse: List of owners with their roles

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not ADMIN
        HTTPException: 404 if restaurant not found
    """
    owners = await service._repository.get_owners_by_restaurant(restaurant_id)

    return OwnershipListSchemaResponse(
        restaurant_id=restaurant_id,
        owners=owners,
        total=len(owners),
    )
