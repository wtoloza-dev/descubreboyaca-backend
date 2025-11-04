"""Find all dishes endpoint (Public).

This module provides an endpoint for finding all dishes of a restaurant.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from ulid import ULID

from app.domains.restaurants.dependencies import get_dish_service_dependency
from app.domains.restaurants.schemas.dish.public.find_all import (
    FindDishesSchemaItem,
    FindDishesSchemaResponse,
)
from app.domains.restaurants.services.dish import DishService
from app.shared.dependencies import get_pagination_dependency
from app.shared.domain.value_objects import Pagination
from app.shared.schemas import PaginationSchemaData


router = APIRouter()


@router.get(
    path="/{restaurant_id}/dishes/",
    status_code=status.HTTP_200_OK,
    summary="Find restaurant dishes",
    description="Retrieve a paginated list of dishes for a specific restaurant with optional filters.",
)
async def handle_find_all(
    restaurant_id: Annotated[
        ULID,
        Path(
            description="ULID of the restaurant",
            examples=["01HQZX123456789ABCDEFGHIJK"],
        ),
    ],
    service: Annotated[DishService, Depends(get_dish_service_dependency)],
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
    category: Annotated[
        str | None,
        Query(
            description="Filter by category",
            examples=["main_course"],
        ),
    ] = None,
    is_available: Annotated[
        bool | None,
        Query(
            description="Filter by availability",
            examples=[True],
        ),
    ] = None,
    is_featured: Annotated[
        bool | None,
        Query(
            description="Filter by featured dishes",
            examples=[True],
        ),
    ] = None,
) -> FindDishesSchemaResponse:
    """Find all dishes for a restaurant with pagination and filters.

    Args:
        restaurant_id: ULID of the restaurant (validated automatically)
        pagination: Pagination entity with page, page_size, offset, and limit
        category: Optional filter by category
        is_available: Optional filter by availability
        is_featured: Optional filter by featured status
        service: Dish service (injected)

    Returns:
        FindDishesSchemaResponse: Paginated list of dishes

    Raises:
        RestaurantNotFoundException: If restaurant not found (handled globally)
        HTTPException 422: If restaurant_id format is invalid (not a valid ULID)

    Example:
        GET /restaurants/{id}/dishes?page=1&page_size=20
        GET /restaurants/{id}/dishes?category=dessert&page=1&page_size=10
    """
    # Build filters dictionary
    filters = {}
    if category is not None:
        filters["category"] = category
    if is_available is not None:
        filters["is_available"] = is_available
    if is_featured is not None:
        filters["is_featured"] = is_featured

    # Get dishes and total count
    dishes, total_count = await service.get_restaurant_dishes(
        restaurant_id=str(restaurant_id),
        filters=filters or None,
        offset=pagination.offset,
        limit=pagination.limit,
    )

    # Convert entities to dicts with JSON-compatible types
    items = [
        FindDishesSchemaItem.model_validate(d.model_dump(mode="json")) for d in dishes
    ]

    return FindDishesSchemaResponse(
        data=items,
        pagination=PaginationSchemaData(
            page=pagination.page,
            page_size=pagination.page_size,
            total=total_count,
        ),
    )
