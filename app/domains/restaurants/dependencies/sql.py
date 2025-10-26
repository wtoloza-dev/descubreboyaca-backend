"""SQL dependencies for the restaurants domain.

This module provides async dependency functions for the restaurants domain.
All dependency functions follow the naming convention: get_{entity}_{type}_dependency
"""

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
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
from app.shared.dependencies import get_async_archive_repository_dependency
from app.shared.dependencies.sql import get_async_session_dependency
from app.shared.domain import AsyncArchiveRepositoryInterface


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


def get_restaurant_service_dependency(
    restaurant_repo: RestaurantRepositoryInterface = Depends(
        get_restaurant_repository_dependency
    ),
    archive_repo: AsyncArchiveRepositoryInterface = Depends(
        get_async_archive_repository_dependency
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

    Returns:
        RestaurantService: Configured service instance with repositories

    Note:
        Both repository and archive_repo receive the same session from their
        respective factories, ensuring they participate in the same transaction.
    """
    return RestaurantService(restaurant_repo, archive_repo)


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
