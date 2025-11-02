"""Dish SQL dependencies.

This module provides async dependency functions for dish operations.
"""

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.restaurants.dependencies.restaurant import (
    get_restaurant_repository_dependency,
)
from app.domains.restaurants.domain.interfaces import (
    DishRepositoryInterface,
    RestaurantRepositoryInterface,
)
from app.domains.restaurants.repositories.dish import (
    DishRepositoryPostgreSQL,
    DishRepositorySQLite,
)
from app.domains.restaurants.services.dish import DishService
from app.domains.audit.dependencies import get_async_archive_repository_dependency
from app.domains.audit.domain import AsyncArchiveRepositoryInterface
from app.shared.dependencies.sql import get_async_session_dependency


def get_dish_repository_dependency(
    session: AsyncSession = Depends(get_async_session_dependency),
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
        return DishRepositorySQLite(session)
    else:
        return DishRepositoryPostgreSQL(session)


def get_dish_service_dependency(
    dish_repo: DishRepositoryInterface = Depends(get_dish_repository_dependency),
    restaurant_repo: RestaurantRepositoryInterface = Depends(
        get_restaurant_repository_dependency
    ),
    archive_repo: AsyncArchiveRepositoryInterface = Depends(
        get_async_archive_repository_dependency
    ),
) -> DishService:
    """Factory to create a dish service with dependencies.

    The service depends on dish, restaurant, and archive repositories to:
    - Validate restaurant existence
    - Maintain referential integrity
    - Archive deleted dishes (Unit of Work pattern)

    Args:
        dish_repo: Dish repository (injected via Depends)
        restaurant_repo: Restaurant repository (injected via Depends)
        archive_repo: Archive repository (injected via Depends)

    Returns:
        DishService: Configured service instance with repositories

    Note:
        All repositories receive the same session from their factories,
        ensuring they participate in the same transaction for Unit of Work.
    """
    return DishService(dish_repo, restaurant_repo, archive_repo)
