"""Review domain dependencies.

This module provides async dependency functions for the reviews domain.
All dependency functions follow the naming convention: get_{entity}_{type}_dependency
"""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.reviews.domain.interfaces import ReviewRepositoryInterface
from app.domains.reviews.repositories import (
    PostgreSQLReviewRepository,
    SQLiteReviewRepository,
)
from app.domains.reviews.services import ReviewService
from app.shared.dependencies.sql import get_async_session_dependency


def get_review_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> ReviewRepositoryInterface:
    """Factory to create a review repository.

    Returns the appropriate repository implementation based on environment.
    Currently uses SQLite for local/development.

    This follows Dependency Inversion Principle: services depend on the
    interface, while this dependency function provides the concrete implementation.

    Args:
        session: Async database session (injected via Depends)

    Returns:
        ReviewRepositoryInterface: Repository instance (SQLite or PostgreSQL)
    """
    if settings.SCOPE == "local":
        return SQLiteReviewRepository(session)
    else:
        return PostgreSQLReviewRepository(session)


def get_review_service_dependency(
    repository: Annotated[
        ReviewRepositoryInterface, Depends(get_review_repository_dependency)
    ],
) -> ReviewService:
    """Factory to create a review service with dependencies.

    The service depends only on repository interfaces, maintaining clean architecture.

    This follows Dependency Inversion Principle and proper layering:
    - Service depends on Repository (one level below)
    - Service does NOT depend on Session (infrastructure detail)

    Args:
        repository: Review repository (injected via Depends)

    Returns:
        ReviewService: Configured service instance with repository

    Note:
        The repository receives the session from its factory,
        ensuring proper transaction management.
    """
    return ReviewService(repository)
