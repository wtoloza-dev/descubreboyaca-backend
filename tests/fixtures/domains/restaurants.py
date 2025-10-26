"""Fixtures for restaurant domain tests.

This module provides domain-specific fixtures for restaurant testing,
including sample data, factory fixtures for creating test entities,
and helper utilities.
"""

from decimal import Decimal

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.domain import DishData, RestaurantData
from app.domains.restaurants.models import (
    DishModel,
    RestaurantModel,
    RestaurantOwnerModel,
)
from app.shared.domain.factories import generate_ulid


@pytest.fixture(name="sample_restaurant_data")
def fixture_sample_restaurant_data() -> RestaurantData:
    """Create sample restaurant data for testing.

    Returns:
        RestaurantData: Complete restaurant data for testing

    Example:
        >>> def test_create(sample_restaurant_data):
        ...     restaurant = service.create(sample_restaurant_data)
        ...     assert restaurant.name == "La Casona Boyacense"
    """
    return RestaurantData(
        name="La Casona Boyacense",
        description="Traditional Colombian cuisine in the heart of Boyacá",
        address="Calle 19 #9-45",
        city="Tunja",
        state="Boyacá",
        country="Colombia",
        phone="+57 300 123 4567",
        email="info@lacasonaboyacense.com",
        website="https://lacasonaboyacense.com",
        location={"latitude": 5.5353, "longitude": -73.3678},
        cuisine_types=["Colombian", "Traditional"],
        price_level="$$",
        features=["Outdoor Seating", "Takeout", "Reservations"],
    )


@pytest.fixture(name="create_test_restaurant")
def fixture_create_test_restaurant(test_session: AsyncSession):
    """Factory fixture to create test restaurants in the database.

    This fixture returns a function that can be called multiple times
    to create different restaurants in the test database.

    Args:
        test_session: Test database session

    Returns:
        Callable: Async function to create restaurants

    Example:
        >>> async def test_list(create_test_restaurant):
        ...     restaurant1 = await create_test_restaurant(
        ...         name="Restaurant 1", city="Tunja"
        ...     )
        ...     restaurant2 = await create_test_restaurant(
        ...         name="Restaurant 2", city="Tunja"
        ...     )
        ...     # Now test listing
    """

    async def _create_restaurant(**kwargs) -> RestaurantModel:
        """Create a restaurant with custom fields.

        Args:
            **kwargs: Fields to override in the restaurant

        Returns:
            RestaurantModel: Created restaurant model
        """
        # Default data
        data = {
            "id": generate_ulid(),  # Generate ULID for the restaurant
            "name": "Test Restaurant",
            "address": "Test Address 123",
            "city": "Tunja",
            "state": "Boyacá",
            "country": "Colombia",
            "phone": "+57 300 000 0000",
            "cuisine_types": [],
            "features": [],
        }
        # Override with provided kwargs
        data.update(kwargs)

        restaurant = RestaurantModel(**data)
        test_session.add(restaurant)
        await test_session.commit()  # Commit to persist to file DB
        await test_session.refresh(restaurant)  # Refresh to get updated data

        return restaurant

    return _create_restaurant


@pytest.fixture(name="create_test_ownership")
def fixture_create_test_ownership(test_session: AsyncSession):
    """Factory fixture to create test restaurant ownership relationships.

    This fixture returns a function that can be called multiple times
    to create ownership relationships between users and restaurants.

    Args:
        test_session: Test database session

    Returns:
        Callable: Async function to create ownerships

    Example:
        >>> async def test_owner_access(create_test_ownership):
        ...     ownership = await create_test_ownership(
        ...         owner_id=user.id,
        ...         restaurant_id=restaurant.id,
        ...         role="owner",
        ...         is_primary=True,
        ...     )
    """

    async def _create_ownership(**kwargs) -> RestaurantOwnerModel:
        """Create an ownership relationship with custom fields.

        Args:
            **kwargs: Fields for the ownership (owner_id, restaurant_id, role, is_primary)

        Returns:
            RestaurantOwnerModel: Created ownership model
        """
        # Default data
        data = {
            "id": generate_ulid(),
            "owner_id": kwargs.get("owner_id", generate_ulid()),
            "restaurant_id": kwargs.get("restaurant_id", generate_ulid()),
            "role": kwargs.get("role", "owner"),
            "is_primary": kwargs.get("is_primary", False),
        }

        ownership = RestaurantOwnerModel(**data)
        test_session.add(ownership)
        await test_session.commit()
        await test_session.refresh(ownership)

        return ownership

    return _create_ownership


@pytest.fixture(name="sample_dish_data")
def fixture_sample_dish_data() -> DishData:
    """Create sample dish data for testing.

    Returns:
        DishData: Complete dish data for testing

    Example:
        >>> def test_create(sample_dish_data):
        ...     dish = service.create(sample_dish_data)
        ...     assert dish.name == "Ajiaco Santafereño"
    """
    return DishData(
        name="Ajiaco Santafereño",
        description="Traditional Colombian chicken and potato soup with corn and capers",
        category="main_course",
        price=Decimal("25000.00"),
        original_price=Decimal("28000.00"),
        is_available=True,
        preparation_time_minutes=45,
        serves=2,
        calories=450,
        image_url="https://example.com/ajiaco.jpg",
        dietary_restrictions=["gluten_free"],
        ingredients=["chicken", "potatoes", "corn", "capers", "cream"],
        allergens=["dairy"],
        flavor_profile={"savory": "high", "creamy": "medium"},
        is_featured=True,
        display_order=1,
    )


@pytest.fixture(name="create_test_dish")
def fixture_create_test_dish(test_session: AsyncSession):
    """Factory fixture to create test dishes in the database.

    This fixture returns a function that can be called multiple times
    to create different dishes in the test database.

    Args:
        test_session: Test database session

    Returns:
        Callable: Async function to create dishes

    Example:
        >>> async def test_list(create_test_dish, create_test_restaurant):
        ...     restaurant = await create_test_restaurant(name="Test Restaurant")
        ...     dish1 = await create_test_dish(
        ...         restaurant_id=restaurant.id, name="Dish 1", category="appetizer"
        ...     )
        ...     dish2 = await create_test_dish(
        ...         restaurant_id=restaurant.id, name="Dish 2", category="main_course"
        ...     )
        ...     # Now test listing
    """

    async def _create_dish(**kwargs) -> DishModel:
        """Create a dish with custom fields.

        Args:
            **kwargs: Fields to override in the dish

        Returns:
            DishModel: Created dish model
        """
        # Default data
        data = {
            "id": generate_ulid(),  # Generate ULID for the dish
            "restaurant_id": kwargs.get("restaurant_id", generate_ulid()),
            "name": "Test Dish",
            "description": "A delicious test dish",
            "category": "main_course",
            "price": Decimal("15000.00"),
            "original_price": None,
            "is_available": True,
            "preparation_time_minutes": 30,
            "serves": 1,
            "calories": 300,
            "image_url": None,
            "dietary_restrictions": [],
            "ingredients": [],
            "allergens": [],
            "flavor_profile": {},
            "is_featured": False,
            "display_order": 0,
        }
        # Override with provided kwargs
        data.update(kwargs)

        dish = DishModel(**data)
        test_session.add(dish)
        await test_session.commit()  # Commit to persist to file DB
        await test_session.refresh(dish)  # Refresh to get updated data

        return dish

    return _create_dish
