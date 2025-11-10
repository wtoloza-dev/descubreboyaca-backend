"""Find dish by ID endpoint (Public).

This module provides an endpoint for finding a single dish by ID.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.restaurants.application.services.dish import DishService
from app.domains.restaurants.infrastructure.dependencies import (
    get_dish_service_dependency,
)
from app.domains.restaurants.presentation.api.schemas.dish.public.find_by_id import (
    FindDishSchemaResponse,
)


router = APIRouter()


@router.get(
    path="/dishes/{dish_id}/",
    status_code=status.HTTP_200_OK,
    summary="Find a dish by ID",
    description="Find complete information about a single dish using its unique ID.",
)
async def handle_find_dish_by_id(
    dish_id: Annotated[
        ULID,
        Path(
            description="ULID of the dish to retrieve",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    service: Annotated[DishService, Depends(get_dish_service_dependency)],
) -> FindDishSchemaResponse:
    """Find a single dish by its ID.

    Args:
        dish_id: ULID of the dish (validated automatically)
        service: Dish service (injected)

    Returns:
        FindDishSchemaResponse: Complete dish information

    Raises:
        DishNotFoundException: If dish not found (handled globally)
        HTTPException 422: If dish_id format is invalid (not a valid ULID)
    """
    dish = await service.find_dish_by_id(str(dish_id))

    return FindDishSchemaResponse.model_validate(dish.model_dump(mode="json"))
