"""Conftest for restaurant domain tests.

This module imports restaurant-specific fixtures from the centralized fixtures package.

For fixture details, see:
    - tests/fixtures/domains/restaurants.py (factories & sample data)
    - tests/fixtures/domains/restaurant_services.py (service layer)
    - tests/fixtures/domains/restaurant_repositories.py (repository layer)
"""

# Import restaurant domain fixtures
# ruff: noqa: F401 (unused imports are intentional - they're fixtures)
from tests.fixtures.domains.restaurant_repositories import (
    fixture_dish_repository,
    fixture_owner_repository,
    fixture_restaurant_repository,
)
from tests.fixtures.domains.restaurant_services import (
    fixture_dish_service,
    fixture_owner_service,
    fixture_restaurant_service,
)
from tests.fixtures.domains.restaurants import (
    fixture_create_test_dish,
    fixture_create_test_ownership,
    fixture_create_test_restaurant,
    fixture_sample_dish_data,
    fixture_sample_restaurant_data,
)
