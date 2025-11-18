"""Update dish endpoint (Owner).

This module provides an endpoint for restaurant owners to update dishes.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_owner_dependency
from app.domains.restaurants.application.use_cases.dish import (
    FindDishByIdUseCase,
    UpdateDishUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    RequireOwnershipUseCase,
)
from app.domains.restaurants.domain import DishData
from app.domains.restaurants.infrastructure.dependencies import (
    get_find_dish_by_id_use_case_dependency,
    get_require_ownership_use_case_dependency,
    get_update_dish_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.dish.owner.update import (
    UpdateDishSchemaRequest,
    UpdateDishSchemaResponse,
)
from app.domains.users.domain import User


router = APIRouter()


@router.patch(
    path="/dishes/{dish_id}/",
    status_code=status.HTTP_200_OK,
    summary="Update a dish",
    description="Update a dish owned/managed by the current user.",
)
async def handle_update_dish(
    dish_id: Annotated[
        ULID,
        Path(
            description="ULID of the dish to update",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    request: Annotated[
        UpdateDishSchemaRequest,
        Body(description="Dish data to update (only provided fields will be updated)"),
    ],
    find_dish_use_case: Annotated[
        FindDishByIdUseCase, Depends(get_find_dish_by_id_use_case_dependency)
    ],
    require_ownership_use_case: Annotated[
        RequireOwnershipUseCase, Depends(get_require_ownership_use_case_dependency)
    ],
    update_dish_use_case: Annotated[
        UpdateDishUseCase, Depends(get_update_dish_use_case_dependency)
    ],
    current_user: Annotated[User, Depends(require_owner_dependency)],
) -> UpdateDishSchemaResponse:
    """Update a dish.

    **Authentication required**: Only users with OWNER role can access.

    This endpoint allows owners/managers to update dishes for their restaurants.
    The current user must be an owner/manager of the restaurant that owns the dish.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        dish_id: ULID of the dish (validated automatically)
        request: Dish data to update (PATCH - only provided fields)
        find_dish_use_case: Find dish by ID use case (injected)
        require_ownership_use_case: Require ownership use case (injected)
        update_dish_use_case: Update dish use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        UpdateDishSchemaResponse: Updated dish details

    Raises:
        InsufficientPermissionsException: If not owner of the restaurant
        DishNotFoundException: If dish not found
        HTTPException 422: If dish_id format is invalid (not a valid ULID)
    """
    # Get dish to verify restaurant ownership
    dish = await find_dish_use_case.execute(str(dish_id))

    # Verify ownership of the restaurant (use case will raise exception if not owner)
    await require_ownership_use_case.execute(
        owner_id=current_user.id,
        restaurant_id=dish.restaurant_id,
    )

    # Get current dish data and merge with updates (PATCH behavior)
    current_data = DishData(**dish.model_dump(exclude={"id", "restaurant_id", "audit"}))
    update_data = request.model_dump(exclude_unset=True)
    merged_data = current_data.model_copy(update=update_data)

    # Update dish
    updated_dish = await update_dish_use_case.execute(
        dish_id=str(dish_id),
        dish_data=merged_data,
        updated_by=current_user.id,
    )

    return UpdateDishSchemaResponse.model_validate(updated_dish.model_dump(mode="json"))
