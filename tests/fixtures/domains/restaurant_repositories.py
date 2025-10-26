"""Repository fixtures for restaurant domain tests.

This module provides repository layer fixtures for testing restaurant domain data access.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.repositories.dish import DishRepositorySQLite
from app.domains.restaurants.repositories.restaurant import (
    RestaurantRepositorySQLite,
)
from app.domains.restaurants.repositories.restaurant_owner import (
    RestaurantOwnerRepositorySQLite,
)


@pytest.fixture(name="restaurant_repository")
def fixture_restaurant_repository(
    test_session: AsyncSession,
) -> RestaurantRepositorySQLite:
    """Create a restaurant repository instance for testing.

    This fixture provides a configured RestaurantRepository for testing
    restaurant data access operations.

    Args:
        test_session: Database session

    Returns:
        RestaurantRepositorySQLite: Configured restaurant repository

    Example:
        >>> async def test_find_by_city(restaurant_repository, create_test_restaurant):
        ...     await create_test_restaurant(name="Restaurant 1", city="Tunja")
        ...     restaurants = await restaurant_repository.find_by_city("Tunja")
        ...     assert len(restaurants) == 1
    """
    return RestaurantRepositorySQLite(test_session)


@pytest.fixture(name="dish_repository")
def fixture_dish_repository(test_session: AsyncSession) -> DishRepositorySQLite:
    """Create a dish repository instance for testing.

    This fixture provides a configured DishRepository for testing
    dish data access operations.

    Args:
        test_session: Database session

    Returns:
        DishRepositorySQLite: Configured dish repository

    Example:
        >>> async def test_find_by_restaurant(
        ...     dish_repository, create_test_restaurant, create_test_dish
        ... ):
        ...     restaurant = await create_test_restaurant()
        ...     await create_test_dish(restaurant_id=restaurant.id)
        ...     dishes = await dish_repository.find_by_restaurant(restaurant.id)
        ...     assert len(dishes) == 1
    """
    return DishRepositorySQLite(test_session)


@pytest.fixture(name="owner_repository")
def fixture_owner_repository(
    test_session: AsyncSession,
) -> RestaurantOwnerRepositorySQLite:
    """Create an owner repository instance for testing.

    This fixture provides a configured RestaurantOwnerRepository for testing
    ownership relationship data access operations.

    Args:
        test_session: Database session

    Returns:
        RestaurantOwnerRepositorySQLite: Configured owner repository

    Example:
        >>> async def test_find_by_owner(
        ...     owner_repository, create_test_ownership, mock_owner_user
        ... ):
        ...     await create_test_ownership(owner_id=mock_owner_user.id)
        ...     ownerships = await owner_repository.find_by_owner(mock_owner_user.id)
        ...     assert len(ownerships) > 0
    """
    return RestaurantOwnerRepositorySQLite(test_session)

