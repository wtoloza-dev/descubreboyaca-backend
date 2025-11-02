"""Archive dependency factories.

This module provides factory functions to create Archive repository
and service instances for dependency injection in FastAPI endpoints.

All dependencies follow the naming convention: get_{entity}_{type}_dependency
"""

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.audit.domain import AsyncArchiveRepositoryInterface
from app.domains.audit.repositories import (
    AsyncArchiveRepositoryPostgreSQL,
    AsyncArchiveRepositorySQLite,
)
from app.domains.audit.services import AsyncArchiveService
from app.shared.dependencies.sql import get_async_session_dependency


def get_async_archive_repository_dependency(
    session: AsyncSession = Depends(get_async_session_dependency),
) -> AsyncArchiveRepositoryInterface:
    """Factory to create an async archive repository instance.

    Returns the appropriate repository implementation based on environment.
    Currently uses SQLite for local/development.

    This follows Dependency Inversion Principle: services depend on the
    interface, while this dependency function provides the concrete implementation.

    Args:
        session: Async SQLModel session (injected via Depends)

    Returns:
        AsyncArchiveRepositoryInterface: Configured async archive repository
    """
    if settings.SCOPE == "local":
        return AsyncArchiveRepositorySQLite(session)
    else:
        return AsyncArchiveRepositoryPostgreSQL(session)


def get_async_archive_service_dependency(
    repository: AsyncArchiveRepositoryInterface = Depends(
        get_async_archive_repository_dependency
    ),
) -> AsyncArchiveService:
    """Factory to create an async archive service instance.

    The service depends only on repository interfaces, not on sessions.
    This follows Dependency Inversion Principle and makes testing easier.

    Args:
        repository: Async archive repository (injected via Depends)

    Returns:
        AsyncArchiveService: Configured async archive service
    """
    return AsyncArchiveService(repository)
