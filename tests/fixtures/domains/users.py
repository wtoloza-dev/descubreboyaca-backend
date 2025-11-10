"""Fixtures for users domain tests.

This module provides domain-specific fixtures for user management tests,
including user service setup, sample data, and user creation helpers.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.audit.infrastructure.persistence.repositories.archive import (
    SQLiteArchiveRepository,
)
from app.domains.auth.application.services import BcryptPasswordHasher
from app.domains.auth.infrastructure.persistence.repositories.user import (
    SQLiteUserRepository,
)
from app.domains.users.application.services import UserService
from app.domains.users.domain.enums import UserRole
from app.domains.users.domain.value_objects import CreateUserData
from app.shared.domain.factories import generate_ulid


@pytest.fixture(name="user_service")
def fixture_user_service(
    test_session: AsyncSession,
) -> UserService:
    """Create a user service instance for testing.

    This fixture provides a fully configured UserService with
    all required dependencies injected.

    Args:
        test_session: Database session

    Returns:
        UserService: Configured user service

    Example:
        >>> async def test_user_creation(user_service):
        ...     user_data = CreateUserData(
        ...         email="test@example.com",
        ...         password="password123",
        ...         full_name="Test User",
        ...     )
        ...     user = await user_service.create(user_data, created_by="admin_id")
        ...     assert user.email == "test@example.com"
    """
    user_repository = SQLiteUserRepository(test_session)
    archive_repository = SQLiteArchiveRepository(test_session)
    password_hasher = BcryptPasswordHasher()

    return UserService(
        user_repository=user_repository,
        archive_repository=archive_repository,
        password_hasher=password_hasher,
    )


@pytest.fixture(name="sample_create_user_data")
def fixture_sample_create_user_data() -> CreateUserData:
    """Provide sample CreateUserData for testing.

    Returns:
        CreateUserData: Sample user creation data

    Example:
        >>> def test_user_creation(sample_create_user_data):
        ...     assert sample_create_user_data.email == "newuser@example.com"
    """
    return CreateUserData(
        email="newuser@example.com",
        password="SecurePassword123!",
        full_name="New Test User",
        role=UserRole.USER,
        is_active=True,
    )


@pytest.fixture(name="create_test_user_admin")
def fixture_create_test_user_admin(
    user_service: UserService,
):
    """Factory fixture for creating test users via UserService.

    This fixture provides a callable that creates users through the
    service layer with customizable attributes.

    Args:
        user_service: User service instance

    Returns:
        Async callable that creates a user through the service

    Example:
        >>> user = await create_test_user_admin(email="test@example.com")
        >>> user = await create_test_user_admin(
        ...     email="admin@example.com", role=UserRole.ADMIN
        ... )
    """

    async def _create(**kwargs):
        """Create a test user through the service.

        Args:
            **kwargs: User attributes to override defaults

        Returns:
            User: Created user entity
        """
        user_data = CreateUserData(
            email=kwargs.get("email", f"user_{generate_ulid()}@test.com"),
            password=kwargs.get("password", "TestPassword123!"),
            full_name=kwargs.get("full_name", "Test User"),
            role=kwargs.get("role", UserRole.USER),
            is_active=kwargs.get("is_active", True),
        )

        created_by = kwargs.get("created_by", generate_ulid())
        return await user_service.create(user_data=user_data, created_by=created_by)

    return _create
