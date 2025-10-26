"""Root conftest for all tests.

This module imports and exposes all global fixtures for the entire test suite.
Fixtures are now organized in the fixtures/ package for better maintainability.

For more details on specific fixtures, see:
    - fixtures/database.py: Database engine and session fixtures
    - fixtures/clients.py: Test client fixtures (with/without auth)
    - fixtures/auth_users.py: Mock user fixtures for auth testing
"""

import asyncio

import pytest

# Import all fixtures to make them available to tests
# ruff: noqa: F401 (unused imports are intentional - they're fixtures)
from tests.fixtures.auth_users import (
    fixture_mock_admin_user,
    fixture_mock_owner_user,
    fixture_mock_regular_user,
)
from tests.fixtures.clients import (
    fixture_admin_client,
    fixture_owner_client,
    fixture_test_client,
    fixture_user_client,
)
from tests.fixtures.database import fixture_test_engine, fixture_test_session


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
