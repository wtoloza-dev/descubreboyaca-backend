"""Test client fixtures with various authentication configurations.

This module provides FastAPI TestClient instances configured for different
authentication scenarios (no auth, admin, owner, regular user).
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession


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
    from app.domains.auth.infrastructure.dependencies.auth import (
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

    Example:
        >>> def test_get_my_restaurants(owner_client):
        ...     response = owner_client.get("/api/v1/restaurants/owner/my")
        ...     assert response.status_code == 200
    """
    from app.domains.auth.infrastructure.dependencies.auth import (
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


@pytest.fixture(name="user_client")
def fixture_user_client(test_session: AsyncSession, mock_regular_user):
    """Create a test client with regular user authentication bypassed.

    This fixture overrides auth dependencies to inject a mock regular user,
    allowing tests to call user-protected endpoints without real JWT tokens.

    Args:
        test_session: Test database session
        mock_regular_user: Mock regular user to inject

    Returns:
        TestClient: Test client with user auth bypassed

    Example:
        >>> def test_user_profile(user_client):
        ...     response = user_client.get("/api/v1/users/me")
        ...     assert response.status_code == 200
    """
    from app.domains.auth.infrastructure.dependencies.auth import (
        get_current_user_dependency,
    )
    from app.main import app
    from app.shared.dependencies.sql import get_async_session_dependency

    async def get_test_session_override():
        yield test_session

    async def get_mock_user():
        return mock_regular_user

    app.dependency_overrides[get_async_session_dependency] = get_test_session_override
    app.dependency_overrides[get_current_user_dependency] = get_mock_user

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
