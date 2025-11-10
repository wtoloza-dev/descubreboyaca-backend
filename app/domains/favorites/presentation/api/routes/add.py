"""Add favorite route handler.

This module handles the endpoint for adding entities to user's favorites.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.auth.infrastructure.dependencies.auth import (
    get_current_user_dependency,
)
from app.domains.favorites.application.services import FavoriteService
from app.domains.favorites.infrastructure.dependencies import (
    get_favorite_service_dependency,
)
from app.domains.favorites.presentation.api.schemas import (
    AddFavoriteSchemaRequest,
    AddFavoriteSchemaResponse,
)
from app.domains.users.domain import User


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Add entity to favorites",
    description="Add a restaurant, dish, or other entity to user's favorites.",
)
async def handle_add_favorite(
    request: Annotated[
        AddFavoriteSchemaRequest,
        Body(description="Request containing entity_type and entity_id"),
    ],
    current_user: Annotated[User, Depends(get_current_user_dependency)],
    service: Annotated[FavoriteService, Depends(get_favorite_service_dependency)],
) -> AddFavoriteSchemaResponse:
    """Add an entity to user's favorites.

    Args:
        request: Request containing entity_type and entity_id
        current_user: Authenticated user from JWT token
        service: Favorite service (injected)

    Returns:
        Created favorite

    Raises:
        FavoriteAlreadyExistsException: If entity is already favorited (409 Conflict)
    """
    # Add favorite (domain exceptions propagate to global handler)
    favorite = await service.add_favorite(
        user_id=current_user.id,
        entity_type=request.entity_type,
        entity_id=request.entity_id,
    )

    return AddFavoriteSchemaResponse(**favorite.model_dump())
