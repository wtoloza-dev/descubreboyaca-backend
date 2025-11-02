"""List restaurants by city endpoint.

This module provides an endpoint for listing restaurants filtered by city with pagination support.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.domains.restaurants.dependencies.restaurant import (
    get_restaurant_service_dependency,
)
from app.domains.restaurants.schemas.restaurant.list import (
    ListRestaurantsSchemaResponse,
    RestaurantSchemaListItem,
)
from app.domains.restaurants.services import RestaurantService
from app.shared.dependencies import get_pagination_dependency
from app.shared.domain.value_objects import Pagination


router = APIRouter()


@router.get(
    path="/city/{city}",
    status_code=status.HTTP_200_OK,
    summary="List restaurants by city",
    description="Retrieve a paginated list of restaurants filtered by city name.",
)
async def handle_list_restaurants_by_city(
    city: Annotated[
        str,
        Path(
            description="City name to filter restaurants",
            examples=["Tunja", "Duitama", "Sogamoso"],
        ),
    ],
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
    service: Annotated[RestaurantService, Depends(get_restaurant_service_dependency)],
) -> ListRestaurantsSchemaResponse:
    """List restaurants by city with pagination.

    Args:
        city: City name to filter restaurants (required path parameter)
        pagination: Pagination entity with page, page_size, offset, and limit
        service: Restaurant service (injected)

    Returns:
        ListRestaurantsSchemaResponse: Paginated list of restaurants in the specified city
    """
    # Get restaurants and total count sequentially to avoid session concurrency issues
    # SQLAlchemy async sessions don't support concurrent operations
    restaurants = await service.list_restaurants_by_city(
        city, offset=pagination.offset, limit=pagination.limit
    )
    total = await service.count_restaurants_by_city(city)

    # Convert entities to dicts with JSON-compatible types (HttpUrl → str)
    items = [
        RestaurantSchemaListItem.model_validate(r.model_dump(mode="json"))
        for r in restaurants
    ]

    return ListRestaurantsSchemaResponse(
        items=items,
        page=pagination.page,
        page_size=pagination.page_size,
        total=total,
    )
