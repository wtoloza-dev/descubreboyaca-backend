"""Restaurant repository dependencies.

This module provides dependency injection factories for restaurant repositories.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface
from app.domains.restaurants.infrastructure.persistence.repositories import (
    PostgreSQLRestaurantRepository,
    SQLiteRestaurantRepository,
)
from app.shared.dependencies.sql import get_async_session_dependency


def get_restaurant_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> RestaurantRepositoryInterface:
    """Factory to create a restaurant repository.

    Returns the appropriate repository implementation based on environment.
    Currently uses SQLite for local/development.

    This follows Dependency Inversion Principle: services depend on the
    interface, while this dependency function provides the concrete implementation.

    Args:
        session: Async database session (injected via Depends)

    Returns:
        RestaurantRepositoryInterface: Repository instance (SQLite or PostgreSQL)
    """
    if settings.SCOPE == "local":
        return SQLiteRestaurantRepository(session)
    else:
        return PostgreSQLRestaurantRepository(session)
