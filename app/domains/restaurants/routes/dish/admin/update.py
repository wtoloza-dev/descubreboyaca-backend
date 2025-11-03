"""Update dish endpoint (Admin).

This module provides an endpoint for administrators to update dishes.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from ulid import ULID

from app.domains.auth.dependencies.auth import require_admin_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies import get_dish_service_dependency
from app.domains.restaurants.domain import DishData
from app.domains.restaurants.schemas.dish.admin.update import (
    UpdateDishSchemaRequest,
    UpdateDishSchemaResponse,
)
from app.domains.restaurants.services.dish import DishService


router = APIRouter()


@router.patch(
    path="/dishes/{dish_id}/",
    status_code=status.HTTP_200_OK,
    summary="Update a dish (Admin)",
    description="Update any dish. Admin only.",
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
    dish_service: DishService = Depends(get_dish_service_dependency),
    current_user: User = Depends(require_admin_dependency),
) -> UpdateDishSchemaResponse:
    """Update a dish.

    **Authentication required**: Only users with ADMIN role can access.

    This endpoint allows administrators to update any dish.
    No ownership verification required.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        dish_id: ULID of the dish (validated automatically)
        request: Dish data to update (PATCH - only provided fields)
        dish_service: Dish service (injected)
        current_user: Authenticated user (injected)

    Returns:
        UpdateDishSchemaResponse: Updated dish details

    Raises:
        DishNotFoundException: If dish not found
        HTTPException 422: If dish_id format is invalid (not a valid ULID)
    """
    # Get current dish
    dish = await dish_service.get_dish_by_id(str(dish_id))

    # Get current dish data and merge with updates (PATCH behavior)
    current_data = DishData(**dish.model_dump(exclude={"id", "restaurant_id", "audit"}))
    update_data = request.model_dump(exclude_unset=True)
    merged_data = current_data.model_copy(update=update_data)

    # Update dish (admins can update any dish)
    updated_dish = await dish_service.update_dish(
        dish_id=str(dish_id),
        dish_data=merged_data,
        updated_by=current_user.id,
    )

    return UpdateDishSchemaResponse.model_validate(updated_dish.model_dump(mode="json"))
