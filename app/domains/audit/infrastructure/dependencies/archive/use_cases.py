"""Archive use cases dependencies.

This module provides dependency injection factories for all archive-related
use cases.
"""

from typing import Annotated

from fastapi import Depends

from app.domains.audit.application.use_cases import (
    ArchiveEntityUseCase,
    FindArchiveByOriginalIdUseCase,
    HardDeleteArchiveByOriginalIdUseCase,
)
from app.domains.audit.domain import ArchiveRepositoryInterface
from app.domains.audit.infrastructure.dependencies.archive.repository import (
    get_archive_repository_dependency,
)


def get_archive_entity_use_case_dependency(
    repository: Annotated[
        ArchiveRepositoryInterface, Depends(get_archive_repository_dependency)
    ],
) -> ArchiveEntityUseCase:
    """Factory to create an ArchiveEntityUseCase instance.

    Args:
        repository: Archive repository (injected via Depends)

    Returns:
        ArchiveEntityUseCase: Configured use case instance
    """
    return ArchiveEntityUseCase(repository)


def get_find_archive_by_original_id_use_case_dependency(
    repository: Annotated[
        ArchiveRepositoryInterface, Depends(get_archive_repository_dependency)
    ],
) -> FindArchiveByOriginalIdUseCase:
    """Factory to create a FindArchiveByOriginalIdUseCase instance.

    Args:
        repository: Archive repository (injected via Depends)

    Returns:
        FindArchiveByOriginalIdUseCase: Configured use case instance
    """
    return FindArchiveByOriginalIdUseCase(repository)


def get_hard_delete_archive_by_original_id_use_case_dependency(
    repository: Annotated[
        ArchiveRepositoryInterface, Depends(get_archive_repository_dependency)
    ],
) -> HardDeleteArchiveByOriginalIdUseCase:
    """Factory to create a HardDeleteArchiveByOriginalIdUseCase instance.

    Args:
        repository: Archive repository (injected via Depends)

    Returns:
        HardDeleteArchiveByOriginalIdUseCase: Configured use case instance
    """
    return HardDeleteArchiveByOriginalIdUseCase(repository)
