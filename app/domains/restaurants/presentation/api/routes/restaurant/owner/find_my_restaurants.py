"""Find my restaurants endpoint.

This module provides an endpoint for restaurant owners to find their restaurants.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domains.auth.infrastructure.dependencies.auth import require_owner_dependency
from app.domains.restaurants.application.use_cases.restaurant import (
    FindRestaurantByIdUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    GetRestaurantsByOwnerUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_find_restaurant_by_id_use_case_dependency,
    get_get_restaurants_by_owner_use_case_dependency,
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
    get_restaurants_use_case: Annotated[
        GetRestaurantsByOwnerUseCase,
        Depends(get_get_restaurants_by_owner_use_case_dependency),
    ],
    find_restaurant_use_case: Annotated[
        FindRestaurantByIdUseCase,
        Depends(get_find_restaurant_by_id_use_case_dependency),
    ],
    current_user: Annotated[User, Depends(require_owner_dependency)],
) -> FindMyRestaurantsSchemaResponse:
    """Find all restaurants owned/managed by the current user.

    **Requiere autenticación**: Solo usuarios con rol OWNER pueden acceder.

    This endpoint returns all restaurants where the current user has ownership
    or management rights, including their role and primary owner status.

    Args:
        get_restaurants_use_case: Get restaurants by owner use case (injected)
        find_restaurant_use_case: Find restaurant by ID use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        FindMyRestaurantsSchemaResponse: List of user's restaurants

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 403 if not OWNER
    """
    # Get ownership relationships
    ownerships = await get_restaurants_use_case.execute(owner_id=current_user.id)

    # Get restaurant details for each ownership
    items: list[FindMyRestaurantsSchemaItem] = []
    for ownership in ownerships:
        restaurant = await find_restaurant_use_case.execute(ownership.restaurant_id)
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
