"""Get dish endpoint (Public).

This module provides an endpoint for retrieving a single dish by ID.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.restaurants.dependencies import get_dish_service_dependency
from app.domains.restaurants.schemas.dish import GetDishSchemaResponse
from app.domains.restaurants.services.dish import DishService


router = APIRouter()


@router.get(
    path="/dishes/{dish_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a dish by ID",
    description="Retrieve complete information about a single dish using its unique ID.",
)
async def handle_get_dish(
    dish_id: Annotated[
        ULID,
        Path(
            description="ULID of the dish to retrieve",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    service: Annotated[DishService, Depends(get_dish_service_dependency)],
) -> GetDishSchemaResponse:
    """Get a single dish by its ID.

    Args:
        dish_id: ULID of the dish (validated automatically)
        service: Dish service (injected)

    Returns:
        GetDishSchemaResponse: Complete dish information

    Raises:
        DishNotFoundException: If dish not found (handled globally)
        HTTPException 422: If dish_id format is invalid (not a valid ULID)
    """
    dish = await service.get_dish_by_id(str(dish_id))

    return GetDishSchemaResponse.model_validate(dish.model_dump(mode="json"))
