"""Delete dish endpoint (Owner).

This module provides an endpoint for restaurant owners to delete dishes.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.dependencies.auth import require_owner_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies import (
    get_dish_service_dependency,
    get_restaurant_owner_service_dependency,
)
from app.domains.restaurants.services import RestaurantOwnerService
from app.domains.restaurants.services.dish import DishService


router = APIRouter()


@router.delete(
    path="/dishes/{dish_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a dish",
    description="Delete a dish owned/managed by the current user.",
)
async def handle_delete_dish(
    dish_id: Annotated[
        ULID,
        Path(
            description="ULID of the dish to delete",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    dish_service: DishService = Depends(get_dish_service_dependency),
    owner_service: RestaurantOwnerService = Depends(
        get_restaurant_owner_service_dependency
    ),
    current_user: User = Depends(require_owner_dependency),
) -> None:
    """Delete a dish.

    **Authentication required**: Only users with OWNER role can access.

    This endpoint allows owners/managers to delete dishes from their restaurants.
    The current user must be an owner/manager of the restaurant that owns the dish.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        dish_id: ULID of the dish (validated automatically)
        dish_service: Dish service (injected)
        owner_service: Restaurant owner service (injected)
        current_user: Authenticated user (injected)

    Returns:
        None: 204 No Content on success

    Raises:
        InsufficientPermissionsException: If not owner of the restaurant
        DishNotFoundException: If dish not found
        HTTPException 422: If dish_id format is invalid (not a valid ULID)
    """
    # Get dish to verify restaurant ownership
    dish = await dish_service.find_dish_by_id(str(dish_id))

    # Verify ownership of the restaurant (service will raise exception if not owner)
    await owner_service.require_ownership(
        owner_id=current_user.id,
        restaurant_id=dish.restaurant_id,
    )

    # Delete dish with archiving (Unit of Work)
    await dish_service.delete_dish(
        dish_id=str(dish_id),
        deleted_by=current_user.id,
    )
