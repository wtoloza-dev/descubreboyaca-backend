"""Find user's favorite restaurants endpoint.

This module provides an authenticated endpoint to find a user's favorite restaurants.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domains.auth.infrastructure.dependencies.auth import (
    get_current_user_dependency,
)
from app.domains.restaurants.application.use_cases.restaurant import (
    ListUserFavoriteRestaurantsUseCase,
)
from app.domains.restaurants.infrastructure.dependencies import (
    get_list_user_favorite_restaurants_use_case_dependency,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.public.find_favorite_restaurants import (
    FindFavoriteRestaurantsSchemaItem,
    FindFavoriteRestaurantsSchemaResponse,
)
from app.domains.users.domain import User
from app.shared.dependencies import get_pagination_dependency
from app.shared.domain.value_objects import Pagination
from app.shared.schemas import PaginationSchemaData


router = APIRouter()


@router.get(
    path="/favorites/",
    status_code=status.HTTP_200_OK,
    summary="Find user's favorite restaurants",
    description="Find all favorite restaurants for the authenticated user. Requires authentication.",
    response_model=FindFavoriteRestaurantsSchemaResponse,
)
async def handle_find_favorite_restaurants(
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
    use_case: Annotated[
        ListUserFavoriteRestaurantsUseCase,
        Depends(get_list_user_favorite_restaurants_use_case_dependency),
    ],
    current_user: Annotated[User, Depends(get_current_user_dependency)],
) -> FindFavoriteRestaurantsSchemaResponse:
    """Find user's favorite restaurants.

    **Authentication required**: This endpoint requires a valid authentication token.

    Args:
        pagination: Pagination entity with page, page_size, offset, and limit
        use_case: List user favorite restaurants use case (injected)
        current_user: Authenticated user (injected)

    Returns:
        Paginated list of user's favorite restaurants

    Raises:
        HTTPException: 401 if not authenticated or token is invalid

    Example:
        GET /api/v1/restaurants/favorites?page=1&page_size=20
        Authorization: Bearer <token>
        → Returns paginated list of user's favorite restaurants
    """
    # Get user's favorite restaurants
    restaurants, total = await use_case.execute(
        user_id=current_user.id,
        offset=pagination.offset,
        limit=pagination.limit,
    )

    # Convert entities to dicts with JSON-compatible types (HttpUrl → str)
    items = [
        FindFavoriteRestaurantsSchemaItem.model_validate(r.model_dump(mode="json"))
        for r in restaurants
    ]

    # Return paginated response
    return FindFavoriteRestaurantsSchemaResponse(
        data=items,
        pagination=PaginationSchemaData(
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        ),
    )
