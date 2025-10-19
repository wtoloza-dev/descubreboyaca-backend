"""Archive dependency factories.

This module provides factory functions to create Archive repository
and service instances for dependency injection in FastAPI endpoints.

Note: Only the Session should use Depends() in routes. Internal layers
(repositories, services) receive dependencies via constructor.
"""

from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.interfaces import (
    ArchiveRepositoryProtocol,
    AsyncArchiveRepositoryProtocol,
)
from app.shared.repositories import ArchiveRepository, AsyncArchiveRepository
from app.shared.services import ArchiveService, AsyncArchiveService


def get_archive_repository(session: Session) -> ArchiveRepository:
    """Factory to create an archive repository instance.

    Args:
        session: SQLModel session (injected in route via Depends)

    Returns:
        ArchiveRepository: Configured archive repository

    Example:
        >>> @app.delete("/restaurants/{id}")
        >>> def delete_restaurant(
        ...     id: str,
        ...     session: Session = Depends(get_sqlite_session_dependency),
        ... ):
        ...     archive_repo = get_archive_repository(session)
        ...     # Use archive_repo
        ...     ...
    """
    return ArchiveRepository(session)


def get_async_archive_repository(session: AsyncSession) -> AsyncArchiveRepository:
    """Factory to create an async archive repository instance.

    Args:
        session: Async SQLModel session (injected in route via Depends)

    Returns:
        AsyncArchiveRepository: Configured async archive repository

    Example:
        >>> @app.delete("/restaurants/{id}")
        >>> async def delete_restaurant(
        ...     id: str,
        ...     session: AsyncSession = Depends(get_async_sqlite_session_dependency),
        ... ):
        ...     archive_repo = get_async_archive_repository(session)
        ...     # Use archive_repo
        ...     ...
    """
    return AsyncArchiveRepository(session)


def get_archive_service(repository: ArchiveRepositoryProtocol) -> ArchiveService:
    """Factory to create an archive service instance.

    Args:
        repository: Archive repository (any implementation of the protocol)

    Returns:
        ArchiveService: Configured archive service

    Example:
        >>> @app.delete("/restaurants/{id}")
        >>> def delete_restaurant(
        ...     id: str,
        ...     session: Session = Depends(get_sqlite_session_dependency),
        ... ):
        ...     archive_repo = get_archive_repository(session)
        ...     archive_service = get_archive_service(archive_repo)
        ...     restaurant = get_restaurant(id)
        ...     archive_service.archive_entity(
        ...         "restaurants", restaurant, note="Deleted"
        ...     )
        ...     # Now delete from main table
        ...     ...
    """
    return ArchiveService(repository)


def get_async_archive_service(
    repository: AsyncArchiveRepositoryProtocol,
) -> AsyncArchiveService:
    """Factory to create an async archive service instance.

    Args:
        repository: Async archive repository (any implementation of the protocol)

    Returns:
        AsyncArchiveService: Configured async archive service

    Example:
        >>> @app.delete("/restaurants/{id}")
        >>> async def delete_restaurant(
        ...     id: str,
        ...     session: AsyncSession = Depends(get_async_sqlite_session_dependency),
        ... ):
        ...     archive_repo = get_async_archive_repository(session)
        ...     archive_service = get_async_archive_service(archive_repo)
        ...     restaurant = await get_restaurant(id)
        ...     await archive_service.archive_entity(
        ...         "restaurants", restaurant, note="Deleted"
        ...     )
        ...     # Now delete from main table
        ...     ...
    """
    return AsyncArchiveService(repository)
