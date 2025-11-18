"""Update my restaurant endpoint.

This module provides an endpoint for restaurant owners to update their restaurant information.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_owner_dependency
from app.domains.restaurants.application.use_cases.restaurant import (
    UpdateRestaurantUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    RequireOwnershipUseCase,
)
from app.domains.restaurants.domain import RestaurantData
from app.domains.restaurants.infrastructure.dependencies import (
    get_require_ownership_use_case_dependency,
    get_update_restaurant_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.owner.update_my_restaurant import (
    UpdateMyRestaurantSchemaRequest,
    UpdateMyRestaurantSchemaResponse,
)
from app.domains.users.domain import User


router = APIRouter()


@router.patch(
    path="/restaurants/{restaurant_id}/",
    status_code=status.HTTP_200_OK,
    summary="Update my restaurant",
    description="Update information about a restaurant owned/managed by the current user.",
)
async def handle_update_my_restaurant(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant to update",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    request: Annotated[
        UpdateMyRestaurantSchemaRequest,
        Body(description="Updated restaurant data (partial for PATCH)"),
    ],
    require_ownership_use_case: Annotated[
        RequireOwnershipUseCase, Depends(get_require_ownership_use_case_dependency)
    ],
    update_restaurant_use_case: Annotated[
        UpdateRestaurantUseCase, Depends(get_update_restaurant_use_case_dependency)
    ],
    current_user: Annotated[User, Depends(require_owner_dependency)],
) -> UpdateMyRestaurantSchemaResponse:
    """Update a restaurant owned/managed by the current user.

    **Authentication required**: Only users with OWNER role can access.

    This endpoint allows owners/managers to update their restaurant information.
    The current user must be an owner/manager of the restaurant.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        restaurant_id: ULID of the restaurant to update
        request: Updated restaurant data
        require_ownership_use_case: Require ownership use case (injected)
        update_restaurant_use_case: Update restaurant use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        UpdateMyRestaurantSchemaResponse: Updated restaurant details

    Raises:
        InsufficientPermissionsException: If not owner of this restaurant
        RestaurantNotFoundException: If restaurant not found
    """
    # Verify ownership (use case will raise exception if not owner)
    await require_ownership_use_case.execute(
        owner_id=current_user.id,
        restaurant_id=str(restaurant_id),
    )

    # Update restaurant (exclude_unset=True for PATCH - only update provided fields)
    restaurant_data = RestaurantData(**request.model_dump(exclude_unset=True))
    updated_restaurant = await update_restaurant_use_case.execute(
        restaurant_id=str(restaurant_id),
        restaurant_data=restaurant_data,
        updated_by=current_user.id,
    )

    return UpdateMyRestaurantSchemaResponse.model_validate(
        updated_restaurant.model_dump(mode="json")
    )
