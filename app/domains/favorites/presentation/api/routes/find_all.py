"""Find all favorites route handler.

This module handles the endpoint for finding all user's favorites.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.domains.auth.infrastructure.dependencies.auth import (
    get_current_user_dependency,
)
from app.domains.favorites.application.services import FavoriteService
from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.infrastructure.dependencies import (
    get_favorite_service_dependency,
)
from app.domains.favorites.presentation.api.schemas import (
    FavoriteSchemaResponse,
    ListFavoritesSchemaResponse,
)
from app.domains.users.domain import User
from app.shared.dependencies.pagination import get_pagination_dependency
from app.shared.domain.value_objects import Pagination
from app.shared.schemas import PaginationSchemaData


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="List user's favorites",
    description="Get a paginated list of user's favorite entities, optionally filtered by type.",
)
async def handle_list_favorites(
    current_user: Annotated[User, Depends(get_current_user_dependency)],
    service: Annotated[FavoriteService, Depends(get_favorite_service_dependency)],
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
    entity_type: EntityType | None = Query(
        default=None, description="Filter by entity type"
    ),
) -> ListFavoritesSchemaResponse:
    """List user's favorites with pagination.

    Args:
        current_user: Authenticated user from JWT token
        service: Favorite service (injected)
        pagination: Pagination value object with page, page_size, offset, and limit
        entity_type: Optional filter by entity type

    Returns:
        Paginated list of favorites
    """
    # List favorites
    favorites, total = await service.list_favorites(
        user_id=current_user.id,
        entity_type=entity_type,
        offset=pagination.offset,
        limit=pagination.limit,
    )

    # Convert to response using model_validate
    items = [FavoriteSchemaResponse.model_validate(favorite) for favorite in favorites]

    return ListFavoritesSchemaResponse(
        data=items,
        pagination=PaginationSchemaData(
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        ),
    )
