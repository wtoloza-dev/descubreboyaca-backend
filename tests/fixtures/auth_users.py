"""Mock user fixtures for authentication testing.

This module provides mock user entities with different roles for testing
protected endpoints without needing real JWT authentication.
"""

import pytest

from app.domains.auth.domain import User
from app.domains.auth.domain.enums import AuthProvider, UserRole
from app.shared.domain.factories import generate_ulid


@pytest.fixture(name="mock_admin_user")
def fixture_mock_admin_user():
    """Create a mock admin user for testing protected endpoints.

    This fixture provides a User entity with ADMIN role for testing
    admin-protected endpoints without needing real JWT authentication.

    Returns:
        User: Mock admin user entity

    Example:
        >>> def test_admin_endpoint(admin_client, mock_admin_user):
        ...     # mock_admin_user is automatically injected by override
        ...     response = admin_client.delete("/api/v1/admin/restaurants/123")
    """
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

    Example:
        >>> def test_owner_endpoint(owner_client, mock_owner_user):
        ...     # mock_owner_user is automatically injected by override
        ...     response = owner_client.get("/api/v1/restaurants/owner/my")
    """
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

    Example:
        >>> def test_user_endpoint(test_client, mock_regular_user):
        ...     response = test_client.get("/api/v1/users/me")
    """
    return User(
        id=generate_ulid(),
        email="user@test.com",
        full_name="Test User",
        role=UserRole.USER,
        auth_provider=AuthProvider.EMAIL,
        is_active=True,
        is_verified=True,
    )
