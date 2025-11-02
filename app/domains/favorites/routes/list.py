"""List favorites route handler.

This module handles the endpoint for listing user's favorites.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.domains.auth.dependencies.auth import get_current_user_dependency
from app.domains.auth.domain import User
from app.domains.favorites.dependencies import get_favorite_service_dependency
from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.schemas import FavoriteResponse, ListFavoritesResponse
from app.domains.favorites.services import FavoriteService
from app.shared.dependencies.pagination import get_pagination_dependency
from app.shared.domain.entities import Pagination


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
) -> ListFavoritesResponse:
    """List user's favorites with pagination.

    Args:
        current_user: Authenticated user from JWT token
        service: Favorite service (injected)
        pagination: Pagination entity with page, page_size, offset, and limit
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
    items = [FavoriteResponse.model_validate(favorite) for favorite in favorites]

    return ListFavoritesResponse(
        items=items,
        page=pagination.page,
        page_size=pagination.page_size,
        total=total,
    )
