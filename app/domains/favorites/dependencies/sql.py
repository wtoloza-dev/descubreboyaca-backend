"""SQL dependency factories for favorites.

This module provides factory functions for creating favorite repositories
and services with their dependencies.
"""

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.favorites.repositories import FavoriteRepository
from app.domains.favorites.services import FavoriteService
from app.shared.dependencies.sql import get_async_session_dependency


def get_favorite_repository_dependency(
    session: AsyncSession = Depends(get_async_session_dependency),
) -> FavoriteRepository:
    """Create a favorite repository instance.

    Args:
        session: Async database session (injected via Depends)

    Returns:
        Configured favorite repository
    """
    return FavoriteRepository(session)


def get_favorite_service_dependency(
    repository: FavoriteRepository = Depends(get_favorite_repository_dependency),
) -> FavoriteService:
    """Create a favorite service instance.

    Args:
        repository: Favorite repository (injected via Depends)

    Returns:
        Configured favorite service
    """
    return FavoriteService(repository)
