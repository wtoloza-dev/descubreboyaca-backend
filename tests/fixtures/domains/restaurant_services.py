"""Service fixtures for restaurant domain tests.

This module provides service layer fixtures for testing restaurant domain business logic.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.audit.application.services import ArchiveService
from app.domains.audit.infrastructure.persistence.repositories import (
    SQLiteArchiveRepository,
)
from app.domains.restaurants.application.services.dish import DishService
from app.domains.restaurants.application.services.restaurant import RestaurantService
from app.domains.restaurants.application.services.restaurant_owner import (
    RestaurantOwnerService,
)
from app.domains.restaurants.infrastructure.persistence.repositories.dish import (
    SQLiteDishRepository,
)
from app.domains.restaurants.infrastructure.persistence.repositories.restaurant import (
    SQLiteRestaurantRepository,
)
from app.domains.restaurants.infrastructure.persistence.repositories.restaurant_owner import (
    SQLiteRestaurantOwnerRepository,
)


@pytest.fixture(name="restaurant_service")
def fixture_restaurant_service(test_session: AsyncSession) -> RestaurantService:
    """Create a restaurant service instance for testing.

    This fixture provides a fully configured RestaurantService with
    the repository dependency injected.

    Args:
        test_session: Database session

    Returns:
        RestaurantService: Configured restaurant service

    Example:
        >>> async def test_create_restaurant(restaurant_service):
        ...     data = RestaurantData(name="Test", city="Tunja")
        ...     restaurant = await restaurant_service.create_restaurant(data)
        ...     assert restaurant.name == "Test"
    """
    repository = SQLiteRestaurantRepository(test_session)
    archive_repository = SQLiteArchiveRepository(test_session)
    archive_service = ArchiveService(archive_repository)
    return RestaurantService(repository, archive_service)


@pytest.fixture(name="dish_service")
def fixture_dish_service(test_session: AsyncSession) -> DishService:
    """Create a dish service instance for testing.

    This fixture provides a fully configured DishService with
    all required dependencies injected.

    Args:
        test_session: Database session

    Returns:
        DishService: Configured dish service

    Example:
        >>> async def test_create_dish(dish_service, create_test_restaurant):
        ...     restaurant = await create_test_restaurant()
        ...     data = DishData(name="Test Dish", price=10.0)
        ...     dish = await dish_service.create_dish(data, restaurant.id)
        ...     assert dish.name == "Test Dish"
    """
    dish_repository = SQLiteDishRepository(test_session)
    restaurant_repository = SQLiteRestaurantRepository(test_session)
    archive_repository = SQLiteArchiveRepository(test_session)
    archive_service = ArchiveService(archive_repository)
    return DishService(dish_repository, restaurant_repository, archive_service)


@pytest.fixture(name="owner_service")
def fixture_owner_service(test_session: AsyncSession) -> RestaurantOwnerService:
    """Create a restaurant owner service instance for testing.

    This fixture provides a fully configured RestaurantOwnerService for testing
    restaurant ownership operations.

    Args:
        test_session: Database session

    Returns:
        RestaurantOwnerService: Configured restaurant owner service

    Example:
        >>> async def test_assign_owner(owner_service):
        ...     await owner_service.assign_owner(
        ...         restaurant_id="123", owner_id="456", role="owner"
        ...     )
    """
    owner_repository = SQLiteRestaurantOwnerRepository(test_session)
    restaurant_repository = SQLiteRestaurantRepository(test_session)
    return RestaurantOwnerService(owner_repository, restaurant_repository)
