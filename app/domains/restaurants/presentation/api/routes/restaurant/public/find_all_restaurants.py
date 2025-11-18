"""Find all restaurants endpoint.

This module provides an endpoint for finding all restaurants with pagination support.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domains.restaurants.application.use_cases.restaurant import (
    FindRestaurantsUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    RestaurantFilters,
    get_find_restaurants_use_case_dependency,
    get_restaurant_filters_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.public.find_all_restaurants import (
    FindAllRestaurantsSchemaItem,
    FindAllRestaurantsSchemaResponse,
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
async def handle_find_all_restaurants(
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
    filters: Annotated[RestaurantFilters, Depends(get_restaurant_filters_dependency)],
    use_case: Annotated[
        FindRestaurantsUseCase, Depends(get_find_restaurants_use_case_dependency)
    ],
) -> FindAllRestaurantsSchemaResponse:
    """Find restaurants with pagination and optional filtering.

    Args:
        pagination: Pagination entity with page, page_size, offset, and limit
        filters: Restaurant filter parameters (injected)
        use_case: Find restaurants use case (injected)

    Returns:
        FindAllRestaurantsSchemaResponse: Paginated list of restaurants

    Example:
        GET /restaurants?page=1&page_size=20
        GET /restaurants?city=Tunja&page=1&page_size=20
        GET /restaurants?city=Tunja&price_level=2&page=1&page_size=10
    """
    # Get restaurants and total count in one call (more efficient)
    restaurants, total = await use_case.execute(
        filters=filters.model_dump(exclude_none=True),
        offset=pagination.offset,
        limit=pagination.limit,
    )

    # Convert entities to dicts with JSON-compatible types (HttpUrl → str)
    items = [
        FindAllRestaurantsSchemaItem.model_validate(r.model_dump(mode="json"))
        for r in restaurants
    ]

    return FindAllRestaurantsSchemaResponse(
        data=items,
        pagination=PaginationSchemaData(
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        ),
    )
