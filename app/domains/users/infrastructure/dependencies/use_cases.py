"""User use case dependencies.

This module provides dependency injection for user use cases.
"""

from typing import Annotated

from fastapi import Depends

from app.domains.audit.domain.interfaces import ArchiveRepositoryInterface
from app.domains.audit.infrastructure.dependencies import (
    get_archive_repository_dependency,
)
from app.domains.auth.domain.interfaces import PasswordHasher
from app.domains.auth.infrastructure.dependencies.security import (
    get_password_hasher_dependency,
)
from app.domains.users.application.use_cases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    FindUsersUseCase,
)
from app.domains.users.domain.interfaces import UserRepositoryInterface
from app.domains.users.infrastructure.dependencies.repository import (
    get_user_repository_dependency,
)


def get_create_user_use_case_dependency(
    user_repository: Annotated[
        UserRepositoryInterface, Depends(get_user_repository_dependency)
    ],
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher_dependency)],
) -> CreateUserUseCase:
    """Factory to create a CreateUserUseCase instance.

    Args:
        user_repository: User repository from dependency
        password_hasher: Password hasher from dependency

    Returns:
        CreateUserUseCase: Configured use case instance
    """
    return CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )


def get_find_users_use_case_dependency(
    user_repository: Annotated[
        UserRepositoryInterface, Depends(get_user_repository_dependency)
    ],
) -> FindUsersUseCase:
    """Factory to create a FindUsersUseCase instance.

    Args:
        user_repository: User repository from dependency

    Returns:
        FindUsersUseCase: Configured use case instance
    """
    return FindUsersUseCase(user_repository=user_repository)


def get_delete_user_use_case_dependency(
    user_repository: Annotated[
        UserRepositoryInterface, Depends(get_user_repository_dependency)
    ],
    archive_repository: Annotated[
        ArchiveRepositoryInterface, Depends(get_archive_repository_dependency)
    ],
) -> DeleteUserUseCase:
    """Factory to create a DeleteUserUseCase instance.

    Args:
        user_repository: User repository from dependency
        archive_repository: Archive repository from dependency

    Returns:
        DeleteUserUseCase: Configured use case instance
    """
    return DeleteUserUseCase(
        user_repository=user_repository,
        archive_repository=archive_repository,
    )
