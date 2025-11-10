"""Find restaurants by city endpoint.

This module provides an endpoint for finding restaurants filtered by city with pagination support.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.domains.restaurants.application.services import RestaurantService
from app.domains.restaurants.infrastructure.dependencies.restaurant import (
    get_restaurant_service_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.public.find_by_city import (
    FindRestaurantsByCitySchemaItem,
    FindRestaurantsByCitySchemaResponse,
)
from app.shared.dependencies import get_pagination_dependency
from app.shared.domain.value_objects import Pagination
from app.shared.schemas import PaginationSchemaData


router = APIRouter()


@router.get(
    path="/city/{city}/",
    status_code=status.HTTP_200_OK,
    summary="Find restaurants by city",
    description="Retrieve a paginated list of restaurants filtered by city name.",
)
async def handle_find_restaurants_by_city(
    city: Annotated[
        str,
        Path(
            description="City name to filter restaurants",
            examples=["Tunja", "Duitama", "Sogamoso"],
        ),
    ],
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
    service: Annotated[RestaurantService, Depends(get_restaurant_service_dependency)],
) -> FindRestaurantsByCitySchemaResponse:
    """Find restaurants by city with pagination.

    Args:
        city: City name to filter restaurants (required path parameter)
        pagination: Pagination entity with page, page_size, offset, and limit
        service: Restaurant service (injected)

    Returns:
        FindRestaurantsByCitySchemaResponse: Paginated list of restaurants in the specified city
    """
    # Get restaurants and total count in one call (more efficient)
    restaurants, total = await service.find_restaurants_by_city(
        city, offset=pagination.offset, limit=pagination.limit
    )

    # Convert entities to dicts with JSON-compatible types (HttpUrl → str)
    items = [
        FindRestaurantsByCitySchemaItem.model_validate(r.model_dump(mode="json"))
        for r in restaurants
    ]

    return FindRestaurantsByCitySchemaResponse(
        data=items,
        pagination=PaginationSchemaData(
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        ),
    )
