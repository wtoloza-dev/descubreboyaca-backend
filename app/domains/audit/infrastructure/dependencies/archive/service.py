"""Archive service dependency.

This module provides the dependency injection factory for the archive service.
Maintained for backward compatibility, but use cases are preferred.
"""

from typing import Annotated

from fastapi import Depends

from app.domains.audit.application.services import ArchiveService
from app.domains.audit.domain import ArchiveRepositoryInterface
from app.domains.audit.infrastructure.dependencies.archive.repository import (
    get_archive_repository_dependency,
)


def get_archive_service_dependency(
    repository: Annotated[
        ArchiveRepositoryInterface, Depends(get_archive_repository_dependency)
    ],
) -> ArchiveService:
    """Factory to create an archive service instance.

    The service depends only on repository interfaces, not on sessions.
    This follows Dependency Inversion Principle and makes testing easier.

    Note: This is maintained for backward compatibility.
    For new features, prefer using specific use cases.

    Args:
        repository: Archive repository (injected via Depends)

    Returns:
        ArchiveService: Configured archive service
    """
    return ArchiveService(repository)
