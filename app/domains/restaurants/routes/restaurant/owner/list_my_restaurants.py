"""List my restaurants endpoint.

This module provides an endpoint for restaurant owners to list their restaurants.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domains.auth.dependencies.auth import require_owner_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.restaurant import (
    get_restaurant_owner_service_dependency,
    get_restaurant_service_dependency,
)
from app.domains.restaurants.schemas.restaurant.owner.list_my_restaurants import (
    ListMyRestaurantsSchemaItem,
    ListMyRestaurantsSchemaResponse,
)
from app.domains.restaurants.services import RestaurantOwnerService, RestaurantService


router = APIRouter()


@router.get(
    path="/restaurants/",
    status_code=status.HTTP_200_OK,
    summary="List my restaurants",
    description="Get a list of all restaurants owned or managed by the current user.",
)
async def handle_list_my_restaurants(
    owner_service: Annotated[
        RestaurantOwnerService, Depends(get_restaurant_owner_service_dependency)
    ],
    restaurant_service: Annotated[
        RestaurantService, Depends(get_restaurant_service_dependency)
    ],
    current_user: Annotated[User, Depends(require_owner_dependency)],
) -> ListMyRestaurantsSchemaResponse:
    """List all restaurants owned/managed by the current user.

    **Requiere autenticación**: Solo usuarios con rol OWNER pueden acceder.

    This endpoint returns all restaurants where the current user has ownership
    or management rights, including their role and primary owner status.

    Args:
        owner_service: Restaurant owner service (injected)
        restaurant_service: Restaurant service (injected)
        current_user: Authenticated user (injected)

    Returns:
        ListMyRestaurantsSchemaResponse: List of user's restaurants

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not OWNER
    """
    # Get ownership relationships
    ownerships = await owner_service.get_restaurants_by_owner(owner_id=current_user.id)

    # Get restaurant details for each ownership
    items: list[ListMyRestaurantsSchemaItem] = []
    for ownership in ownerships:
        restaurant = await restaurant_service.get_restaurant_by_id(
            ownership.restaurant_id
        )
        items.append(
            ListMyRestaurantsSchemaItem(
                restaurant_id=restaurant.id,
                restaurant_name=restaurant.name,
                role=ownership.role,
                is_primary=ownership.is_primary,
                city=restaurant.city,
                state=restaurant.state,
            )
        )

    return ListMyRestaurantsSchemaResponse(
        items=items,
        total=len(items),
    )
