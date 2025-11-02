"""Restaurant domain dependencies.

This module provides async dependency functions for the restaurants domain.
All dependency functions follow the naming convention: get_{entity}_{type}_dependency
"""

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.favorites.domain.interfaces import FavoriteRepositoryInterface
from app.domains.favorites.repositories import FavoriteRepository
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface
from app.domains.restaurants.repositories import (
    RestaurantOwnerRepositoryPostgreSQL,
    RestaurantOwnerRepositorySQLite,
    RestaurantRepositoryPostgreSQL,
    RestaurantRepositorySQLite,
)
from app.domains.restaurants.services import (
    RestaurantOwnerService,
    RestaurantService,
)
from app.domains.audit.dependencies import get_async_archive_repository_dependency
from app.domains.audit.domain import AsyncArchiveRepositoryInterface
from app.shared.dependencies.sql import get_async_session_dependency


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
        return RestaurantRepositorySQLite(session)
    else:
        return RestaurantRepositoryPostgreSQL(session)


def get_favorite_repository_for_restaurant_dependency(
    session: AsyncSession = Depends(get_async_session_dependency),
) -> FavoriteRepositoryInterface:
    """Factory to create a favorite repository for restaurant operations.

    This dependency is specifically used by the restaurant service when it needs
    to interact with favorites. It uses the same session as other repositories
    to ensure transaction consistency.

    Args:
        session: Async database session (injected via Depends)

    Returns:
        FavoriteRepositoryInterface: Repository instance
    """
    return FavoriteRepository(session)


def get_restaurant_service_dependency(
    restaurant_repo: RestaurantRepositoryInterface = Depends(
        get_restaurant_repository_dependency
    ),
    archive_repo: AsyncArchiveRepositoryInterface = Depends(
        get_async_archive_repository_dependency
    ),
    favorite_repo: FavoriteRepositoryInterface = Depends(
        get_favorite_repository_for_restaurant_dependency
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
        restaurant_repo: Restaurant repository (injected via Depends)
        archive_repo: Archive repository (injected via Depends)
        favorite_repo: Favorite repository (injected via Depends)

    Returns:
        RestaurantService: Configured service instance with repositories

    Note:
        All repositories receive the same session from their respective factories,
        ensuring they participate in the same transaction.
    """
    return RestaurantService(restaurant_repo, archive_repo, favorite_repo)


def get_restaurant_owner_repository_dependency(
    session: AsyncSession = Depends(get_async_session_dependency),
) -> RestaurantOwnerRepositorySQLite | RestaurantOwnerRepositoryPostgreSQL:
    """Factory to create a restaurant owner repository.

    Returns the appropriate repository implementation based on environment.

    Args:
        session: Async database session (injected via Depends)

    Returns:
        RestaurantOwnerRepository: Repository instance (SQLite or PostgreSQL)
    """
    if settings.SCOPE == "local":
        return RestaurantOwnerRepositorySQLite(session)
    else:
        return RestaurantOwnerRepositoryPostgreSQL(session)


def get_restaurant_owner_service_dependency(
    owner_repo: RestaurantOwnerRepositorySQLite
    | RestaurantOwnerRepositoryPostgreSQL = Depends(
        get_restaurant_owner_repository_dependency
    ),
) -> RestaurantOwnerService:
    """Factory to create a restaurant owner service with dependencies.

    The service depends only on repository interfaces, not on sessions.
    This follows Dependency Inversion Principle and makes testing easier.

    Args:
        owner_repo: Restaurant owner repository (injected via Depends)

    Returns:
        RestaurantOwnerService: Configured service instance with repositories
    """
    return RestaurantOwnerService(owner_repo)
