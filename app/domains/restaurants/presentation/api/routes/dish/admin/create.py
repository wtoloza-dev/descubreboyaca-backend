"""Create dish endpoint (Admin).

This module provides an endpoint for administrators to create dishes.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from ulid import ULID

from app.domains.auth.infrastructure.dependencies.auth import require_admin_dependency
from app.domains.restaurants.application.use_cases.dish import CreateDishUseCase
from app.domains.restaurants.domain import DishData
from app.domains.restaurants.infrastructure.dependencies import (
    get_create_dish_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.dish.admin.create import (
    CreateDishSchemaRequest,
    CreateDishSchemaResponse,
)
from app.domains.users.domain import User


router = APIRouter()


@router.post(
    path="/restaurants/{restaurant_id}/dishes/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new dish (Admin)",
    description="Create a new dish for any restaurant. Admin only.",
)
async def handle_create_dish(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    request: Annotated[
        CreateDishSchemaRequest,
        Body(description="Dish data to create"),
    ],
    use_case: Annotated[
        CreateDishUseCase, Depends(get_create_dish_use_case_dependency)
    ],
    current_user: Annotated[User, Depends(require_admin_dependency)],
) -> CreateDishSchemaResponse:
    """Create a new dish for a restaurant.

    **Authentication required**: Only users with ADMIN role can access.

    This endpoint allows administrators to create dishes for any restaurant.
    No ownership verification required.

    Domain exceptions are allowed to propagate and will be handled by the
    centralized exception handler in app.core.errors.

    Args:
        restaurant_id: ULID of the restaurant (validated automatically)
        request: Dish data
        use_case: Create dish use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        CreateDishSchemaResponse: Created dish details

    Raises:
        RestaurantNotFoundException: If restaurant not found
        HTTPException 422: If restaurant_id format is invalid (not a valid ULID)
    """
    # Create dish (admins can create for any restaurant)
    dish_data = DishData(**request.model_dump())
    created_dish = await use_case.execute(
        dish_data=dish_data,
        restaurant_id=str(restaurant_id),
        created_by=current_user.id,
    )

    return CreateDishSchemaResponse.model_validate(created_dish.model_dump(mode="json"))
