"""Restaurant domain dependencies.

This module provides async dependency functions for the restaurants domain.
All dependency functions follow the naming convention: get_{entity}_{type}_dependency
"""

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.audit.dependencies import get_archive_repository_dependency
from app.domains.audit.domain import ArchiveRepositoryInterface
from app.domains.favorites.dependencies import get_favorite_repository_dependency
from app.domains.favorites.domain.interfaces import FavoriteRepositoryInterface
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface
from app.domains.restaurants.repositories import (
    PostgreSQLRestaurantOwnerRepository,
    PostgreSQLRestaurantRepository,
    SQLiteRestaurantOwnerRepository,
    SQLiteRestaurantRepository,
)
from app.domains.restaurants.services import (
    RestaurantOwnerService,
    RestaurantService,
)
from app.shared.dependencies.sql import get_async_session_dependency


# ================================
# Repositories
# ================================


def get_restaurant_repository_dependency(
    session: AsyncSession = Depends(get_async_session_dependency),
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


def get_restaurant_owner_repository_dependency(
    session: AsyncSession = Depends(get_async_session_dependency),
) -> SQLiteRestaurantOwnerRepository | PostgreSQLRestaurantOwnerRepository:
    """Factory to create a restaurant owner repository.

    Returns the appropriate repository implementation based on environment.

    Args:
        session: Async database session (injected via Depends)

    Returns:
        RestaurantOwnerRepository: Repository instance (SQLite or PostgreSQL)
    """
    if settings.SCOPE == "local":
        return SQLiteRestaurantOwnerRepository(session)
    else:
        return PostgreSQLRestaurantOwnerRepository(session)


# ================================
# Services
# ================================


def get_restaurant_service_dependency(
    restaurant_repository: RestaurantRepositoryInterface = Depends(
        get_restaurant_repository_dependency
    ),
    archive_repository: ArchiveRepositoryInterface = Depends(
        get_archive_repository_dependency
    ),
    favorite_repository: FavoriteRepositoryInterface = Depends(
        get_favorite_repository_dependency
    ),
) -> RestaurantService:
    """Factory to create a restaurant service with dependencies.

    The service depends only on repository interfaces, maintaining clean architecture.
    When the service needs the database session for Unit of Work operations,
    it obtains it from the repository itself.

    This follows Dependency Inversion Principle and proper layering:
    - Service depends on Repository (one level below)
    - Service does NOT depend on Session (infrastructure detail)

    Args:
        restaurant_repository: Restaurant repository (injected via Depends)
        archive_repository: Archive repository (injected via Depends)
        favorite_repository: Favorite repository (injected via Depends)

    Returns:
        RestaurantService: Configured service instance with repositories

    Note:
        All repositories receive the same session from their respective factories,
        ensuring they participate in the same transaction.
    """
    return RestaurantService(
        restaurant_repository, archive_repository, favorite_repository
    )


def get_restaurant_owner_service_dependency(
    owner_repository: SQLiteRestaurantOwnerRepository
    | PostgreSQLRestaurantOwnerRepository = Depends(
        get_restaurant_owner_repository_dependency
    ),
) -> RestaurantOwnerService:
    """Factory to create a restaurant owner service with dependencies.

    The service depends only on repository interfaces, not on sessions.
    This follows Dependency Inversion Principle and makes testing easier.

    Args:
        owner_repository: Restaurant owner repository (injected via Depends)

    Returns:
        RestaurantOwnerService: Configured service instance with repositories
    """
    return RestaurantOwnerService(owner_repository)
