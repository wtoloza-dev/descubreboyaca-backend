"""Add favorite route handler.

This module handles the endpoint for adding entities to user's favorites.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.auth.dependencies.auth import get_current_user_dependency
from app.domains.auth.domain import User
from app.domains.favorites.dependencies import get_favorite_service_dependency
from app.domains.favorites.domain.exceptions import FavoriteAlreadyExistsError
from app.domains.favorites.schemas import AddFavoriteRequest, AddFavoriteResponse
from app.domains.favorites.services import FavoriteService


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Add entity to favorites",
    description="Add a restaurant, dish, or other entity to user's favorites.",
)
async def handle_add_favorite(
    request: Annotated[
        AddFavoriteRequest,
        Body(description="Request containing entity_type and entity_id"),
    ],
    current_user: Annotated[User, Depends(get_current_user_dependency)],
    service: Annotated[FavoriteService, Depends(get_favorite_service_dependency)],
) -> AddFavoriteResponse:
    """Add an entity to user's favorites.

    Args:
        request: Request containing entity_type and entity_id
        current_user: Authenticated user from JWT token
        service: Favorite service (injected)

    Returns:
        Created favorite

    Raises:
        FavoriteAlreadyExistsError: If entity is already favorited (409 Conflict)
    """
    # Add favorite
    try:
        favorite = await service.add_favorite(
            user_id=current_user.id,
            entity_type=request.entity_type,
            entity_id=request.entity_id,
        )
    except FavoriteAlreadyExistsError:
        # Re-raise to be handled by error handler
        raise

    return AddFavoriteResponse(**favorite.model_dump())
