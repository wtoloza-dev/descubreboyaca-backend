"""Find my restaurants endpoint.

This module provides an endpoint for restaurant owners to find their restaurants.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domains.auth.infrastructure.dependencies.auth import require_owner_dependency
from app.domains.restaurants.application.services import (
    RestaurantOwnerService,
    RestaurantService,
)
from app.domains.restaurants.infrastructure.dependencies.restaurant import (
    get_restaurant_owner_service_dependency,
    get_restaurant_service_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.owner.find_my_restaurants import (
    FindMyRestaurantsSchemaItem,
    FindMyRestaurantsSchemaResponse,
)
from app.domains.users.domain import User


router = APIRouter()


@router.get(
    path="/restaurants/",
    status_code=status.HTTP_200_OK,
    summary="Find my restaurants",
    description="Find all restaurants owned or managed by the current user.",
)
async def handle_find_my_restaurants(
    owner_service: Annotated[
        RestaurantOwnerService, Depends(get_restaurant_owner_service_dependency)
    ],
    restaurant_service: Annotated[
        RestaurantService, Depends(get_restaurant_service_dependency)
    ],
    current_user: Annotated[User, Depends(require_owner_dependency)],
) -> FindMyRestaurantsSchemaResponse:
    """Find all restaurants owned/managed by the current user.

    **Requiere autenticación**: Solo usuarios con rol OWNER pueden acceder.

    This endpoint returns all restaurants where the current user has ownership
    or management rights, including their role and primary owner status.

    Args:
        owner_service: Restaurant owner service (injected)
        restaurant_service: Restaurant service (injected)
        current_user: Authenticated user (injected)

    Returns:
        FindMyRestaurantsSchemaResponse: List of user's restaurants

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not OWNER
    """
    # Get ownership relationships
    ownerships = await owner_service.get_restaurants_by_owner(owner_id=current_user.id)

    # Get restaurant details for each ownership
    items: list[FindMyRestaurantsSchemaItem] = []
    for ownership in ownerships:
        restaurant = await restaurant_service.find_restaurant_by_id(
            ownership.restaurant_id
        )
        items.append(
            FindMyRestaurantsSchemaItem(
                restaurant_id=restaurant.id,
                restaurant_name=restaurant.name,
                role=ownership.role,
                is_primary=ownership.is_primary,
                city=restaurant.city,
                state=restaurant.state,
            )
        )

    return FindMyRestaurantsSchemaResponse(
        items=items,
        total=len(items),
    )
