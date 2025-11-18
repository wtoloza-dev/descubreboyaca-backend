"""Find my restaurant endpoint.

This module provides an endpoint for restaurant owners to find their restaurant details.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_owner_dependency
from app.domains.restaurants.application.use_cases.restaurant import (
    FindRestaurantByIdUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    RequireOwnershipUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_find_restaurant_by_id_use_case_dependency,
    get_require_ownership_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.owner.find_my_restaurant import (
    FindMyRestaurantSchemaResponse,
)
from app.domains.users.domain import User


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
    require_ownership_use_case: Annotated[
        RequireOwnershipUseCase, Depends(get_require_ownership_use_case_dependency)
    ],
    find_restaurant_use_case: Annotated[
        FindRestaurantByIdUseCase,
        Depends(get_find_restaurant_by_id_use_case_dependency),
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
        require_ownership_use_case: Require ownership use case (injected)
        find_restaurant_use_case: Find restaurant by ID use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        FindMyRestaurantSchemaResponse: Restaurant details

    Raises:
        InsufficientPermissionsException: If not owner of this restaurant
        RestaurantNotFoundException: If restaurant not found
    """
    # Verify ownership (use case will raise exception if not owner)
    await require_ownership_use_case.execute(
        owner_id=current_user.id,
        restaurant_id=str(restaurant_id),
    )

    # Get restaurant details
    restaurant = await find_restaurant_use_case.execute(str(restaurant_id))

    return FindMyRestaurantSchemaResponse.model_validate(
        restaurant.model_dump(mode="json")
    )
