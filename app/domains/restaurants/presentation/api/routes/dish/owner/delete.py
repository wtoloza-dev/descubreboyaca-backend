"""Delete dish endpoint (Owner).

This module provides an endpoint for restaurant owners to delete dishes.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_owner_dependency
from app.domains.restaurants.application.use_cases.dish import (
    DeleteDishUseCase,
    FindDishByIdUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    RequireOwnershipUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_delete_dish_use_case_dependency,
    get_find_dish_by_id_use_case_dependency,
    get_require_ownership_use_case_dependency,
)
from app.domains.users.domain import User


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
    find_dish_use_case: Annotated[
        FindDishByIdUseCase, Depends(get_find_dish_by_id_use_case_dependency)
    ],
    require_ownership_use_case: Annotated[
        RequireOwnershipUseCase, Depends(get_require_ownership_use_case_dependency)
    ],
    delete_dish_use_case: Annotated[
        DeleteDishUseCase, Depends(get_delete_dish_use_case_dependency)
    ],
    current_user: Annotated[User, Depends(require_owner_dependency)],
) -> None:
    """Delete a dish.

    **Authentication required**: Only users with OWNER role can access.

    This endpoint allows owners/managers to delete dishes from their restaurants.
    The current user must be an owner/manager of the restaurant that owns the dish.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        dish_id: ULID of the dish (validated automatically)
        find_dish_use_case: Find dish by ID use case (injected)
        require_ownership_use_case: Require ownership use case (injected)
        delete_dish_use_case: Delete dish use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        None: 204 No Content on success

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

    # Delete dish with archiving (Unit of Work)
    await delete_dish_use_case.execute(
        dish_id=str(dish_id),
        deleted_by=current_user.id,
    )
