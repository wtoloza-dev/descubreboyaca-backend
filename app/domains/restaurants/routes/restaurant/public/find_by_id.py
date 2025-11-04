"""Find restaurant by ID endpoint.

This module provides an endpoint for finding a single restaurant by ID.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.restaurants.dependencies.restaurant import (
    get_restaurant_service_dependency,
)
from app.domains.restaurants.schemas.restaurant.public.find_by_id import (
    FindRestaurantSchemaResponse,
)
from app.domains.restaurants.services import RestaurantService


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
    service: Annotated[RestaurantService, Depends(get_restaurant_service_dependency)],
) -> FindRestaurantSchemaResponse:
    """Find a single restaurant by its ID.

    Args:
        restaurant_id: ULID of the restaurant (validated automatically)
        service: Restaurant service (injected)

    Returns:
        FindRestaurantSchemaResponse: Complete restaurant information

    Raises:
        RestaurantNotFoundException: If restaurant not found (handled globally)
        HTTPException 422: If restaurant_id format is invalid (not a valid ULID)
    """
    # Convert ULID to string for service layer
    restaurant = await service.find_restaurant_by_id(str(restaurant_id))

    # Convert entity to dict with JSON-compatible types (HttpUrl → str)
    return FindRestaurantSchemaResponse.model_validate(
        restaurant.model_dump(mode="json")
    )
