"""User service dependencies.

This module provides dependency injection for user service operations.
"""

from typing import Annotated

from fastapi import Depends

from app.domains.audit.dependencies import get_archive_repository_dependency
from app.domains.audit.domain.interfaces import ArchiveRepositoryInterface
from app.domains.auth.dependencies.security import get_password_hasher_dependency
from app.domains.auth.dependencies.sql import get_user_repository_dependency
from app.domains.auth.domain.interfaces import UserRepositoryInterface
from app.domains.auth.services import BcryptPasswordHasher
from app.domains.users.services import UserService


def get_user_service_dependency(
    user_repository: Annotated[
        UserRepositoryInterface, Depends(get_user_repository_dependency)
    ],
    archive_repository: Annotated[
        ArchiveRepositoryInterface, Depends(get_archive_repository_dependency)
    ],
    password_hasher: Annotated[
        BcryptPasswordHasher, Depends(get_password_hasher_dependency)
    ],
) -> UserService:
    """Get user service instance.

    This dependency provides a fully configured UserService with all required
    repositories and services for user management operations.

    Args:
        user_repository: User repository from dependency
        archive_repository: Archive repository from dependency
        password_hasher: Password hasher from dependency

    Returns:
        UserService: Configured user service instance
    """
    return UserService(
        user_repository=user_repository,
        archive_repository=archive_repository,
        password_hasher=password_hasher,
    )
