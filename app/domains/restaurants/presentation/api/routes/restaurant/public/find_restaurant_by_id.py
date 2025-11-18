"""Find restaurant by ID endpoint.

This module provides an endpoint for finding a single restaurant by ID.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.restaurants.application.use_cases.restaurant import (
    FindRestaurantByIdUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_find_restaurant_by_id_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.public.find_restaurant_by_id import (
    FindRestaurantByIdSchemaResponse,
)


router = APIRouter()


@router.get(
    path="/{restaurant_id}/",
    status_code=status.HTTP_200_OK,
    summary="Find a restaurant by ID",
    description="Find complete information about a single restaurant using its unique ID.",
)
async def handle_find_restaurant_by_id(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant to retrieve",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    use_case: Annotated[
        FindRestaurantByIdUseCase,
        Depends(get_find_restaurant_by_id_use_case_dependency),
    ],
) -> FindRestaurantByIdSchemaResponse:
    """Find a single restaurant by its ID.

    Args:
        restaurant_id: ULID of the restaurant (validated automatically)
        use_case: Find restaurant by ID use case (injected)

    Returns:
        FindRestaurantByIdSchemaResponse: Complete restaurant information

    Raises:
        RestaurantNotFoundException: If restaurant not found (handled globally)
        HTTPException 422: If restaurant_id format is invalid (not a valid ULID)
    """
    # Convert ULID to string and execute use case
    restaurant = await use_case.execute(str(restaurant_id))

    # Convert entity to dict with JSON-compatible types (HttpUrl → str)
    return FindRestaurantByIdSchemaResponse.model_validate(
        restaurant.model_dump(mode="json")
    )
