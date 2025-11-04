"""Find my restaurant endpoint.

This module provides an endpoint for restaurant owners to find their restaurant details.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.dependencies.auth import require_owner_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.restaurant import (
    get_restaurant_owner_service_dependency,
    get_restaurant_service_dependency,
)
from app.domains.restaurants.schemas.restaurant.owner.find_my_restaurant import (
    FindMyRestaurantSchemaResponse,
)
from app.domains.restaurants.services import RestaurantOwnerService, RestaurantService


router = APIRouter()


@router.get(
    path="/restaurants/{restaurant_id}/",
    status_code=status.HTTP_200_OK,
    summary="Find my restaurant details",
    description="Find detailed information about a restaurant owned/managed by the current user.",
)
async def handle_find_my_restaurant(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    owner_service: Annotated[
        RestaurantOwnerService, Depends(get_restaurant_owner_service_dependency)
    ],
    restaurant_service: Annotated[
        RestaurantService, Depends(get_restaurant_service_dependency)
    ],
    current_user: Annotated[User, Depends(require_owner_dependency)],
) -> FindMyRestaurantSchemaResponse:
    """Find details of a restaurant owned/managed by the current user.

    **Authentication required**: Only users with OWNER role can access.

    This endpoint returns detailed information about a specific restaurant.
    The current user must be an owner/manager/staff of the restaurant.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        restaurant_id: ULID of the restaurant
        owner_service: Restaurant owner service (injected)
        restaurant_service: Restaurant service (injected)
        current_user: Authenticated user (injected)

    Returns:
        FindMyRestaurantSchemaResponse: Restaurant details

    Raises:
        InsufficientPermissionsException: If not owner of this restaurant
        RestaurantNotFoundException: If restaurant not found
    """
    # Verify ownership (service will raise exception if not owner)
    await owner_service.require_ownership(
        owner_id=current_user.id,
        restaurant_id=str(restaurant_id),
    )

    # Get restaurant details
    restaurant = await restaurant_service.find_restaurant_by_id(str(restaurant_id))

    return FindMyRestaurantSchemaResponse.model_validate(
        restaurant.model_dump(mode="json")
    )
