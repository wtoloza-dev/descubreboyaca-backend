"""Find all restaurants endpoint.

This module provides an endpoint for finding all restaurants with pagination support.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domains.restaurants.application.services import RestaurantService
from app.domains.restaurants.infrastructure.dependencies import (
    RestaurantFilters,
    get_restaurant_filters_dependency,
    get_restaurant_service_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.public.find_all import (
    FindRestaurantsSchemaItem,
    FindRestaurantsSchemaResponse,
)
from app.shared.dependencies import get_pagination_dependency
from app.shared.domain.value_objects import Pagination
from app.shared.schemas import PaginationSchemaData


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Find all restaurants",
    description="Retrieve a paginated list of all restaurants. "
    "Results can be filtered using query parameters (city, state, country, price_level).",
)
async def handle_find_all(
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
    filters: Annotated[RestaurantFilters, Depends(get_restaurant_filters_dependency)],
    service: Annotated[RestaurantService, Depends(get_restaurant_service_dependency)],
) -> FindRestaurantsSchemaResponse:
    """Find restaurants with pagination and optional filtering.

    Args:
        pagination: Pagination entity with page, page_size, offset, and limit
        filters: Restaurant filter parameters (injected)
        service: Restaurant service (injected)

    Returns:
        FindRestaurantsSchemaResponse: Paginated list of restaurants

    Example:
        GET /restaurants?page=1&page_size=20
        GET /restaurants?city=Tunja&page=1&page_size=20
        GET /restaurants?city=Tunja&price_level=2&page=1&page_size=10
    """
    # Get restaurants and total count in one call (more efficient)
    restaurants, total = await service.find_restaurants(
        filters=filters.model_dump(exclude_none=True),
        offset=pagination.offset,
        limit=pagination.limit,
    )

    # Convert entities to dicts with JSON-compatible types (HttpUrl → str)
    items = [
        FindRestaurantsSchemaItem.model_validate(r.model_dump(mode="json"))
        for r in restaurants
    ]

    return FindRestaurantsSchemaResponse(
        data=items,
        pagination=PaginationSchemaData(
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        ),
    )
