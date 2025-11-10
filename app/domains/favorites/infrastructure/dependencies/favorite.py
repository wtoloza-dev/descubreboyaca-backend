"""Favorite dependency factories.

This module provides factory functions for creating favorite repositories
and services with their dependencies.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.favorites.application.services import FavoriteService
from app.domains.favorites.domain.interfaces import FavoriteRepositoryInterface
from app.domains.favorites.infrastructure.persistence.repositories import (
    PostgreSQLFavoriteRepository,
    SQLiteFavoriteRepository,
)
from app.shared.dependencies.sql import get_async_session_dependency


def get_favorite_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> FavoriteRepositoryInterface:
    """Create a favorite repository instance.

    Returns the appropriate repository implementation based on environment.
    Currently uses SQLite for local/development.

    Args:
        session: Async database session (injected via Depends)

    Returns:
        FavoriteRepositoryInterface: Repository instance (SQLite or PostgreSQL)
    """
    if settings.SCOPE == "local":
        return SQLiteFavoriteRepository(session)
    else:
        return PostgreSQLFavoriteRepository(session)


def get_favorite_service_dependency(
    repository: Annotated[
        FavoriteRepositoryInterface, Depends(get_favorite_repository_dependency)
    ],
) -> FavoriteService:
    """Create a favorite service instance.

    Args:
        repository: Favorite repository (injected via Depends)

    Returns:
        FavoriteService: Configured favorite service
    """
    return FavoriteService(repository)
