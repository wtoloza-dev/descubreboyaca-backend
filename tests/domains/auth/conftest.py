"""Conftest for auth domain tests.

This module imports auth-specific fixtures from the centralized fixtures package.

For fixture details, see:
    - tests/fixtures/domains/auth.py
"""

# Import auth domain fixtures
# ruff: noqa: F401 (unused imports are intentional - they're fixtures)
from tests.fixtures.domains.auth import (
    fixture_auth_service,
    fixture_create_test_user,
    fixture_password_service,
    fixture_test_password,
    fixture_token_provider,
    fixture_user_repository,
)
