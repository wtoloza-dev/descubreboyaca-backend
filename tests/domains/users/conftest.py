"""Conftest for users domain tests.

This module imports user-specific fixtures from the centralized fixtures package.

For fixture details, see:
    - tests/fixtures/domains/users.py (factories & sample data)
    - tests/fixtures/domains/auth.py (auth fixtures for user creation)
"""

# Import user domain fixtures
# ruff: noqa: F401 (unused imports are intentional - they're fixtures)
from tests.fixtures.domains.auth import (
    fixture_create_test_user,
    fixture_test_password,
    fixture_user_repository,
)
from tests.fixtures.domains.users import (
    fixture_create_test_user_admin,
    fixture_sample_create_user_data,
    fixture_user_service,
)
