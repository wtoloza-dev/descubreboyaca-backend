"""User repository dependencies.

This module provides dependency injection factories for user repositories.
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.users.domain.interfaces import UserRepositoryInterface
from app.domains.users.infrastructure.persistence.repositories import (
    PostgreSQLUserRepository,
    SQLiteUserRepository,
)
from app.shared.dependencies.sql import get_async_session_dependency


def get_user_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> UserRepositoryInterface:
    """Factory to create a user repository.

    Returns the appropriate repository implementation based on environment.
    Currently uses SQLite for local/development.

    This follows Dependency Inversion Principle: use cases depend on the
    interface, while this dependency function provides the concrete implementation.

    Args:
        session: Async database session (injected via Depends)

    Returns:
        UserRepositoryInterface: Repository instance (SQLite or PostgreSQL)
    """
    if settings.SCOPE == "local":
        return SQLiteUserRepository(session)
    else:
        return PostgreSQLUserRepository(session)
