"""List restaurants by city endpoint.

This module provides an endpoint for listing restaurants filtered by city with pagination support.
"""

from fastapi import APIRouter, Depends, Path, status

from app.domains.restaurants.dependencies.sql import get_restaurant_service_dependency
from app.domains.restaurants.schemas.list import (
    ListRestaurantsSchemaResponse,
    RestaurantSchemaListItem,
)
from app.domains.restaurants.services import RestaurantService
from app.shared.dependencies import get_pagination_params_dependency
from app.shared.domain import PaginationParams


router = APIRouter()


@router.get(
    path="/city/{city}",
    status_code=status.HTTP_200_OK,
    summary="List restaurants by city",
    description="Retrieve a paginated list of restaurants filtered by city name.",
)
async def handle_list_restaurants_by_city(
    city: str = Path(
        ...,
        description="City name to filter restaurants",
        examples=["Tunja", "Duitama", "Sogamoso"],
    ),
    pagination: PaginationParams = Depends(get_pagination_params_dependency),
    service: RestaurantService = Depends(get_restaurant_service_dependency),
) -> ListRestaurantsSchemaResponse:
    """List restaurants by city with pagination.

    Args:
        city: City name to filter restaurants (required path parameter)
        pagination: Pagination parameters (page, page_size converted to offset, limit)
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

    # Calculate current page from offset and limit
    page = (pagination.offset // pagination.limit) + 1

    return ListRestaurantsSchemaResponse(
        items=items,
        page=page,
        page_size=pagination.limit,
        total=total,
    )
