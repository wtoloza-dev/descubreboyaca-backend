"""Remove favorite route handler.

This module handles the endpoint for removing entities from user's favorites.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.domains.auth.dependencies.auth import get_current_user_dependency
from app.domains.auth.domain import User
from app.domains.favorites.dependencies import get_favorite_service_dependency
from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.services import FavoriteService


router = APIRouter()


@router.delete(
    path="/{entity_type}/{entity_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove entity from favorites",
    description="Remove a restaurant, dish, or other entity from user's favorites.",
)
async def handle_remove_favorite(
    entity_type: Annotated[
        EntityType, Path(description="Type of entity (restaurant, dish, etc.)")
    ],
    entity_id: Annotated[str, Path(description="ULID of the entity")],
    current_user: Annotated[User, Depends(get_current_user_dependency)],
    service: Annotated[FavoriteService, Depends(get_favorite_service_dependency)],
) -> None:
    """Remove an entity from user's favorites.

    Args:
        entity_type: Type of entity (restaurant, dish, etc.)
        entity_id: ULID of the entity
        current_user: Authenticated user from JWT token
        service: Favorite service (injected)

    Raises:
        FavoriteNotFoundException: If favorite not found (404 Not Found)
    """
    # Remove favorite (domain exceptions propagate to global handler)
    await service.remove_favorite(
        user_id=current_user.id,
        entity_type=entity_type,
        entity_id=entity_id,
    )
