"""Check favorite route handler.

This module handles the endpoint for checking if an entity is favorited.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.domains.auth.infrastructure.dependencies.auth import (
    get_current_user_dependency,
)
from app.domains.favorites.application.services import FavoriteService
from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.infrastructure.dependencies import (
    get_favorite_service_dependency,
)
from app.domains.favorites.presentation.api.schemas import CheckFavoriteSchemaResponse
from app.domains.users.domain import User


router = APIRouter()


@router.get(
    path="/{entity_type}/{entity_id}/is-favorite/",
    status_code=status.HTTP_200_OK,
    summary="Check if entity is favorited",
    description="Check whether a specific entity is in user's favorites.",
)
async def handle_check_favorite(
    entity_type: Annotated[
        EntityType, Path(description="Type of entity (restaurant, dish, etc.)")
    ],
    entity_id: Annotated[str, Path(description="ULID of the entity")],
    current_user: Annotated[User, Depends(get_current_user_dependency)],
    service: Annotated[FavoriteService, Depends(get_favorite_service_dependency)],
) -> CheckFavoriteSchemaResponse:
    """Check if an entity is favorited by the user.

    Args:
        entity_type: Type of entity (restaurant, dish, etc.)
        entity_id: ULID of the entity
        current_user: Authenticated user from JWT token
        service: Favorite service (injected)

    Returns:
        Response indicating if entity is favorited
    """
    # Check favorite
    favorite = await service.check_favorite(
        user_id=current_user.id,
        entity_type=entity_type,
        entity_id=entity_id,
    )

    return CheckFavoriteSchemaResponse(
        is_favorite=favorite is not None,
        favorite_id=favorite.id if favorite else None,
    )
