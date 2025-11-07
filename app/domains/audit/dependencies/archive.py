"""Archive dependency factories.

This module provides factory functions to create Archive repository
and service instances for dependency injection in FastAPI endpoints.

All dependencies follow the naming convention: get_{entity}_{type}_dependency
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.audit.domain import ArchiveRepositoryInterface
from app.domains.audit.repositories import (
    PostgreSQLArchiveRepository,
    SQLiteArchiveRepository,
)
from app.domains.audit.services import ArchiveService
from app.shared.dependencies.sql import get_async_session_dependency


def get_archive_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> ArchiveRepositoryInterface:
    """Factory to create an archive repository instance.

    Returns the appropriate repository implementation based on environment.
    Currently uses SQLite for local/development.

    This follows Dependency Inversion Principle: services depend on the
    interface, while this dependency function provides the concrete implementation.

    Args:
        session: Async SQLModel session (injected via Depends)

    Returns:
        ArchiveRepositoryInterface: Configured archive repository
    """
    if settings.SCOPE == "local":
        return SQLiteArchiveRepository(session)
    else:
        return PostgreSQLArchiveRepository(session)


def get_archive_service_dependency(
    repository: Annotated[
        ArchiveRepositoryInterface, Depends(get_archive_repository_dependency)
    ],
) -> ArchiveService:
    """Factory to create an archive service instance.

    The service depends only on repository interfaces, not on sessions.
    This follows Dependency Inversion Principle and makes testing easier.

    Args:
        repository: Archive repository (injected via Depends)

    Returns:
        ArchiveService: Configured archive service
    """
    return ArchiveService(repository)
