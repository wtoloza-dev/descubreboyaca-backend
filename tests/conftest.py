"""Root conftest for all tests.

This module contains all global fixtures for the entire test suite.
Fixtures defined here are available to all test modules automatically.

Following SQLModel testing best practices from:
https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/
"""

import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


# ============================================================================
# PYTEST HELPERS
# ============================================================================


class PytestHelpers:
    """Helper methods for pytest tests."""

    @staticmethod
    def run_async(coro):
        """Run an async coroutine in a sync test.

        Args:
            coro: Coroutine to run

        Returns:
            Result of the coroutine

        Example:
            >>> user = pytest.helpers.run_async(
            ...     create_test_user(email="test@example.com")
            ... )
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)


@pytest.fixture(scope="session")
def helpers():
    """Provide helper methods to tests."""
    return PytestHelpers()


# Make helpers available as pytest.helpers
pytest.helpers = PytestHelpers()


@pytest.fixture(name="test_engine", scope="function")
async def fixture_test_engine():
    """Create a test database engine with file-based SQLite.

    Each test gets a fresh file-based database that is automatically cleaned up.
    Using file DB instead of in-memory to avoid transaction isolation issues with TestClient.

    Returns:
        AsyncEngine: Async engine for testing
    """
    import os
    import tempfile

    # Import all models to ensure they're registered with SQLModel
    from app.domains.auth.models import UserModel  # noqa: F401
    from app.domains.restaurants.models import (  # noqa: F401
        RestaurantModel,
        RestaurantOwnerModel,
    )
    from app.shared.models import ArchiveModel  # noqa: F401

    # Create temporary file for test database
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    # Create file-based database engine
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        echo=False,  # Set to True for SQL debugging
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    await engine.dispose()

    # Clean up temp file
    try:
        os.unlink(db_path)
    except Exception:
        pass


@pytest.fixture(name="test_session", scope="function")
async def fixture_test_session(test_engine):
    """Create a test database session.

    This fixture provides a clean async database session for each test.
    The session shares the same engine as test_client to ensure data visibility.

    Args:
        test_engine: Test database engine

    Returns:
        AsyncSession: Async session for testing

    Example:
        >>> async def test_create_restaurant(test_session):
        ...     restaurant = RestaurantModel(name="Test")
        ...     test_session.add(restaurant)
        ...     await test_session.commit()
    """
    async with AsyncSession(test_engine, expire_on_commit=False) as session:
        yield session


@pytest.fixture(name="test_client")
def fixture_test_client(test_session: AsyncSession):
    """Create a FastAPI test client with test database.

    This fixture creates a TestClient with the database dependency
    overridden to use the SAME session as the test. This ensures
    data visibility between test setup and API calls.

    Args:
        test_session: Test database session (shared with test)

    Returns:
        TestClient: FastAPI test client configured for testing

    Example:
        >>> def test_api_endpoint(test_client):
        ...     response = test_client.get("/api/v1/restaurants")
        ...     assert response.status_code == 200
    """
    from app.main import app
    from app.shared.dependencies.sql import get_async_session_dependency

    # Override to return THE SAME session instance used by the test
    # Must be async generator to match production dependency signature
    async def get_test_session_override():
        yield test_session

    # Override the single session dependency - all repositories use this
    app.dependency_overrides[get_async_session_dependency] = get_test_session_override

    with TestClient(app) as client:
        yield client

    # Clean up overrides
    app.dependency_overrides.clear()


# ============================================================================
# AUTH FIXTURES (for testing protected endpoints without real JWT)
# ============================================================================


@pytest.fixture(name="mock_admin_user")
def fixture_mock_admin_user():
    """Create a mock admin user for testing protected endpoints.

    This fixture provides a User entity with ADMIN role for testing
    admin-protected endpoints without needing real JWT authentication.

    Returns:
        User: Mock admin user entity

    Example:
        >>> def test_admin_endpoint(test_client, mock_admin_user):
        ...     # mock_admin_user is automatically injected by override
        ...     response = test_client.delete("/api/v1/admin/restaurants/123")
    """
    from app.domains.auth.domain import User
    from app.domains.auth.domain.enums import AuthProvider, UserRole
    from app.shared.domain.factories import generate_ulid

    return User(
        id=generate_ulid(),
        email="admin@test.com",
        full_name="Test Admin",
        role=UserRole.ADMIN,
        auth_provider=AuthProvider.EMAIL,
        is_active=True,
        is_verified=True,
    )


@pytest.fixture(name="mock_owner_user")
def fixture_mock_owner_user():
    """Create a mock owner user for testing protected endpoints.

    This fixture provides a User entity with OWNER role for testing
    owner-protected endpoints without needing real JWT authentication.

    Returns:
        User: Mock owner user entity
    """
    from app.domains.auth.domain import User
    from app.domains.auth.domain.enums import AuthProvider, UserRole
    from app.shared.domain.factories import generate_ulid

    return User(
        id=generate_ulid(),
        email="owner@test.com",
        full_name="Test Owner",
        role=UserRole.OWNER,
        auth_provider=AuthProvider.EMAIL,
        is_active=True,
        is_verified=True,
    )


@pytest.fixture(name="mock_regular_user")
def fixture_mock_regular_user():
    """Create a mock regular user for testing protected endpoints.

    This fixture provides a User entity with USER role for testing
    user-protected endpoints without needing real JWT authentication.

    Returns:
        User: Mock regular user entity
    """
    from app.domains.auth.domain import User
    from app.domains.auth.domain.enums import AuthProvider, UserRole
    from app.shared.domain.factories import generate_ulid

    return User(
        id=generate_ulid(),
        email="user@test.com",
        full_name="Test User",
        role=UserRole.USER,
        auth_provider=AuthProvider.EMAIL,
        is_active=True,
        is_verified=True,
    )


@pytest.fixture(name="admin_client")
def fixture_admin_client(test_session: AsyncSession, mock_admin_user):
    """Create a test client with admin authentication bypassed.

    This fixture overrides auth dependencies to inject a mock admin user,
    allowing tests to call admin-protected endpoints without real JWT tokens.

    **Separation of Concerns**: We're testing the endpoint logic, not auth.
    Auth has its own tests.

    Args:
        test_session: Test database session
        mock_admin_user: Mock admin user to inject

    Returns:
        TestClient: Test client with admin auth bypassed

    Example:
        >>> def test_delete_restaurant(admin_client):
        ...     response = admin_client.delete("/api/v1/admin/restaurants/123")
        ...     assert response.status_code == 204
    """
    from app.domains.auth.dependencies.auth import (
        get_current_user_dependency,
        require_admin_dependency,
    )
    from app.main import app
    from app.shared.dependencies.sql import get_async_session_dependency

    # Override session dependency
    async def get_test_session_override():
        yield test_session

    # Override auth dependencies to return mock admin user
    async def get_mock_admin():
        return mock_admin_user

    app.dependency_overrides[get_async_session_dependency] = get_test_session_override
    app.dependency_overrides[get_current_user_dependency] = get_mock_admin
    app.dependency_overrides[require_admin_dependency] = get_mock_admin

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="owner_client")
def fixture_owner_client(test_session: AsyncSession, mock_owner_user):
    """Create a test client with owner authentication bypassed.

    This fixture overrides auth dependencies to inject a mock owner user,
    allowing tests to call owner-protected endpoints without real JWT tokens.

    Args:
        test_session: Test database session
        mock_owner_user: Mock owner user to inject

    Returns:
        TestClient: Test client with owner auth bypassed
    """
    from app.domains.auth.dependencies.auth import (
        get_current_user_dependency,
        require_owner_dependency,
    )
    from app.main import app
    from app.shared.dependencies.sql import get_async_session_dependency

    async def get_test_session_override():
        yield test_session

    async def get_mock_owner():
        return mock_owner_user

    app.dependency_overrides[get_async_session_dependency] = get_test_session_override
    app.dependency_overrides[get_current_user_dependency] = get_mock_owner
    app.dependency_overrides[require_owner_dependency] = get_mock_owner

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
