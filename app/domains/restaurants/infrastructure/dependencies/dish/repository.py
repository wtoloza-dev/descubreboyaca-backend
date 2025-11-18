"""Dish repository dependencies.

This module provides dependency injection factories for dish repositories.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.restaurants.domain.interfaces import DishRepositoryInterface
from app.domains.restaurants.infrastructure.persistence.repositories.dish import (
    PostgreSQLDishRepository,
    SQLiteDishRepository,
)
from app.shared.dependencies.sql import get_async_session_dependency


def get_dish_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> DishRepositoryInterface:
    """Factory to create a dish repository.

    Returns the appropriate repository implementation based on environment.
    Currently uses SQLite for local/development.

    Args:
        session: Async database session (injected via Depends)

    Returns:
        DishRepositoryInterface: Repository instance (SQLite or PostgreSQL)
    """
    if settings.SCOPE == "local":
        return SQLiteDishRepository(session)
    else:
        return PostgreSQLDishRepository(session)
