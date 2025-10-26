"""List restaurants endpoint.

This module provides an endpoint for listing restaurants with pagination support.
"""

from fastapi import APIRouter, Depends, status

from app.domains.restaurants.dependencies import (
    RestaurantFilters,
    get_restaurant_filters_dependency,
    get_restaurant_service_dependency,
)
from app.domains.restaurants.schemas.restaurant.list import (
    ListRestaurantsSchemaResponse,
    RestaurantSchemaListItem,
)
from app.domains.restaurants.services import RestaurantService
from app.shared.dependencies import get_pagination_params_dependency
from app.shared.domain import PaginationParams


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List all restaurants",
    description="Retrieve a paginated list of all restaurants. "
    "Results can be filtered using query parameters (city, state, country, price_level).",
)
async def handle_list_restaurants(
    pagination: PaginationParams = Depends(get_pagination_params_dependency),
    filters: RestaurantFilters = Depends(get_restaurant_filters_dependency),
    service: RestaurantService = Depends(get_restaurant_service_dependency),
) -> ListRestaurantsSchemaResponse:
    """List restaurants with pagination and optional filtering.

    Args:
        pagination: Pagination parameters (page, page_size converted to offset, limit)
        filters: Restaurant filter parameters (injected)
        service: Restaurant service (injected)

    Returns:
        ListRestaurantsSchemaResponse: Paginated list of restaurants

    Example:
        GET /restaurants?page=1&page_size=20
        GET /restaurants?city=Tunja&page=1&page_size=20
        GET /restaurants?city=Tunja&price_level=2&page=1&page_size=10
    """
    # Convert filters to dictionary, excluding None values (using Pydantic native method)
    filter_dict = filters.model_dump(exclude_none=True)

    # Get restaurants with filters through service layer
    restaurants = await service.find_restaurants(
        filters=filter_dict or None,
        offset=pagination.offset,
        limit=pagination.limit,
    )

    # Get total count with same filters through service layer
    total = await service.count_restaurants(filters=filter_dict or None)

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
