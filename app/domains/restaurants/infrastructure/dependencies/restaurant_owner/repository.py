"""Restaurant owner repository dependencies.

This module provides dependency injection factories for restaurant owner repositories.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)
from app.domains.restaurants.infrastructure.persistence.repositories import (
    PostgreSQLRestaurantOwnerRepository,
    SQLiteRestaurantOwnerRepository,
)
from app.shared.dependencies.sql import get_async_session_dependency


def get_restaurant_owner_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> RestaurantOwnerRepositoryInterface:
    """Factory to create a restaurant owner repository.

    Returns the appropriate repository implementation based on environment.

    Args:
        session: Async database session (injected via Depends)

    Returns:
        RestaurantOwnerRepositoryInterface: Repository instance (SQLite or PostgreSQL)
    """
    if settings.SCOPE == "local":
        return SQLiteRestaurantOwnerRepository(session)
    else:
        return PostgreSQLRestaurantOwnerRepository(session)
