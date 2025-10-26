"""SQL dependencies.

This module provides dependency injection factories for auth repositories
and services that require database access.

All dependency functions follow the naming convention: get_{entity}_{type}_dependency
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.domains.auth.dependencies.security import (
    get_password_hasher_dependency,
    get_token_provider_dependency,
)
from app.domains.auth.domain.interfaces import UserRepositoryInterface
from app.domains.auth.repositories import (
    UserRepositoryPostgreSQL,
    UserRepositorySQLite,
)
from app.domains.auth.services import (
    AuthService,
    BcryptPasswordHasher,
    JWTTokenProvider,
)
from app.shared.dependencies.sql import get_async_session_dependency


def get_user_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> UserRepositoryInterface:
    """Get user repository instance.

    Returns the appropriate repository implementation based on environment.
    Currently uses SQLite for local/development.
    For production, this can be swapped to UserRepositoryPostgreSQL.

    This follows Dependency Inversion Principle: services depend on the
    interface, while this dependency function provides the concrete implementation.

    Args:
        session: Database session from dependency

    Returns:
        UserRepositoryInterface: Repository instance (SQLite or PostgreSQL)
    """
    if settings.SCOPE == "local":
        return UserRepositorySQLite(session)
    else:
        return UserRepositoryPostgreSQL(session)


def get_auth_service_dependency(
    user_repository: Annotated[
        UserRepositoryInterface, Depends(get_user_repository_dependency)
    ],
    token_provider: Annotated[JWTTokenProvider, Depends(get_token_provider_dependency)],
    password_hasher: Annotated[
        BcryptPasswordHasher, Depends(get_password_hasher_dependency)
    ],
) -> AuthService:
    """Get auth service instance.

    Args:
        user_repository: User repository from dependency
        token_provider: Token provider from dependency
        password_hasher: Password hasher from dependency

    Returns:
        AuthService instance
    """
    return AuthService(
        user_repository=user_repository,
        token_provider=token_provider,
        password_hasher=password_hasher,
    )
