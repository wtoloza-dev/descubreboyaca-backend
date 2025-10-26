"""Update my restaurant endpoint.

This module provides an endpoint for restaurant owners to update their restaurant information.
"""

from fastapi import APIRouter, Depends, status

from app.domains.auth.dependencies.auth import require_owner_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.sql import (
    get_restaurant_owner_service_dependency,
    get_restaurant_service_dependency,
)
from app.domains.restaurants.domain import RestaurantData
from app.domains.restaurants.schemas.create import CreateRestaurantSchemaRequest
from app.domains.restaurants.schemas.get import GetRestaurantSchemaResponse
from app.domains.restaurants.services import RestaurantOwnerService, RestaurantService


router = APIRouter()


@router.patch(
    path="/restaurants/{restaurant_id}",
    status_code=status.HTTP_200_OK,
    summary="Update my restaurant",
    description="Update information about a restaurant owned/managed by the current user.",
)
async def handle_update_my_restaurant(
    restaurant_id: str,
    request: CreateRestaurantSchemaRequest,
    owner_service: RestaurantOwnerService = Depends(
        get_restaurant_owner_service_dependency
    ),
    restaurant_service: RestaurantService = Depends(get_restaurant_service_dependency),
    current_user: User = Depends(require_owner_dependency),
) -> GetRestaurantSchemaResponse:
    """Update a restaurant owned/managed by the current user.

    **Authentication required**: Only users with OWNER role can access.

    This endpoint allows owners/managers to update their restaurant information.
    The current user must be an owner/manager of the restaurant.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        restaurant_id: ULID of the restaurant to update
        request: Updated restaurant data
        owner_service: Restaurant owner service (injected)
        restaurant_service: Restaurant service (injected)
        current_user: Authenticated user (injected)

    Returns:
        GetRestaurantSchemaResponse: Updated restaurant details

    Raises:
        InsufficientPermissionsException: If not owner of this restaurant
        RestaurantNotFoundException: If restaurant not found
    """
    # Verify ownership (service will raise exception if not owner)
    await owner_service.require_ownership(
        owner_id=current_user.id,
        restaurant_id=restaurant_id,
    )

    # Update restaurant (exclude_unset=True for PATCH - only update provided fields)
    restaurant_data = RestaurantData(**request.model_dump(exclude_unset=True))
    updated_restaurant = await restaurant_service.update_restaurant(
        restaurant_id=restaurant_id,
        restaurant_data=restaurant_data,
        updated_by=current_user.id,
    )

    return GetRestaurantSchemaResponse.model_validate(
        updated_restaurant.model_dump(mode="json")
    )
