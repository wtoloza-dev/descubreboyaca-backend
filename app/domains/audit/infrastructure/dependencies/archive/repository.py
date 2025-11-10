"""Archive repository dependency.

This module provides the dependency injection factory for the archive repository.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.audit.domain import ArchiveRepositoryInterface
from app.domains.audit.infrastructure.persistence.repositories import (
    PostgreSQLArchiveRepository,
    SQLiteArchiveRepository,
)
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
