"""Delete dish endpoint (Admin).

This module provides an endpoint for administrators to delete dishes.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.restaurants.application.use_cases.dish import DeleteDishUseCase
from app.domains.restaurants.infrastructure.dependencies import (
    get_delete_dish_use_case_dependency,
)
from app.domains.users.domain import User


router = APIRouter()


@router.delete(
    path="/dishes/{dish_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a dish (Admin)",
    description="Delete any dish. Admin only.",
)
async def handle_delete_dish(
    dish_id: Annotated[
        ULID,
        Path(
            description="ULID of the dish to delete",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    use_case: Annotated[
        DeleteDishUseCase, Depends(get_delete_dish_use_case_dependency)
    ],
    current_user: Annotated[User, Depends(require_admin_dependency)],
) -> None:
    """Delete a dish.

    **Authentication required**: Only users with ADMIN role can access.

    This endpoint allows administrators to delete any dish.
    No ownership verification required.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        dish_id: ULID of the dish (validated automatically)
        use_case: Delete dish use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        None: 204 No Content on success

    Raises:
        DishNotFoundException: If dish not found
        HTTPException 422: If dish_id format is invalid (not a valid ULID)
    """
    # Delete dish with archiving (admins can delete any dish)
    await use_case.execute(
        dish_id=str(dish_id),
        deleted_by=current_user.id,
    )
