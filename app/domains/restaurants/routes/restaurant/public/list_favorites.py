"""List user's favorite restaurants endpoint.

This module provides an authenticated endpoint to list a user's favorite restaurants.
"""

from fastapi import APIRouter, Depends, status

from app.domains.auth.dependencies.auth import get_current_user_dependency
from app.domains.auth.domain import User
from app.domains.restaurants.dependencies.sql import get_restaurant_service_dependency
from app.domains.restaurants.services import RestaurantService


router = APIRouter()


@router.get(
    path="/favorites",
    status_code=status.HTTP_200_OK,
    summary="List user's favorite restaurants",
    description="List all favorite restaurants for the authenticated user. Requires authentication.",
)
async def handle_list_with_favorites(
    service: RestaurantService = Depends(get_restaurant_service_dependency),
    current_user: User = Depends(get_current_user_dependency),
):
    """List user's favorite restaurants.

    **Authentication required**: This endpoint requires a valid authentication token.

    Args:
        service: Restaurant service (injected)
        current_user: Authenticated user (injected)

    Returns:
        List of user's favorite restaurants

    Raises:
        HTTPException: 401 if not authenticated or token is invalid

    Example:
        GET /api/v1/restaurants/favorites
        Authorization: Bearer <token>
        → Returns list of user's favorite restaurants
    """
    # TODO: Implement actual logic
    # restaurants = await service.list_user_favorites(current_user.id)

    return {
        "message": f"Showing favorites for user {current_user.email}",
        "user_id": current_user.id,
        "restaurants": [],  # TODO: Implement
    }
