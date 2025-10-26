"""Unit tests for Restaurant domain entities.

Tests pure domain logic without database or external dependencies.
Uses mocks where necessary to isolate business logic.
"""

from datetime import UTC, datetime

import pytest
from pydantic import HttpUrl, ValidationError

from app.domains.restaurants.domain.entities import Restaurant, RestaurantData
from app.shared.domain import GeoLocation


class TestRestaurantData:
    """Unit tests for RestaurantData value object (pure domain logic)."""

    def test_create_restaurant_data_with_valid_minimal_data(self):
        """Test creating restaurant data with minimal required fields.

        Given: Minimal valid restaurant data (name, address, city, phone)
        When: Creating RestaurantData instance
        Then: Instance is created successfully with defaults
        """
        # Arrange & Act
        restaurant_data = RestaurantData(
            name="Test Restaurant",
            address="Calle 1 #2-3",
            city="Tunja",
            phone="+57 300 123 4567",
        )

        # Assert
        assert restaurant_data.name == "Test Restaurant"
        assert restaurant_data.address == "Calle 1 #2-3"
        assert restaurant_data.city == "Tunja"
        assert restaurant_data.phone == "+57 300 123 4567"
        # Verify defaults
        assert restaurant_data.state == "Boyacá"
        assert restaurant_data.country == "Colombia"
        assert restaurant_data.cuisine_types == []
        assert restaurant_data.features == []
        assert restaurant_data.description is None

    def test_create_restaurant_data_with_complete_data(self):
        """Test creating restaurant data with all fields populated.

        Given: Complete restaurant data including optional fields
        When: Creating RestaurantData instance
        Then: All fields are set correctly
        """
        # Arrange & Act
        restaurant_data = RestaurantData(
            name="La Casona Boyacense",
            description="Restaurante típico de comida boyacense",
            address="Calle 20 #10-52",
            city="Tunja",
            state="Boyacá",
            postal_code="150001",
            country="Colombia",
            phone="+57 300 123 4567",
            email="lacasona@example.com",
            website=HttpUrl("https://lacasona.com"),
            location=GeoLocation(latitude=5.5353, longitude=-73.3678),
            cuisine_types=["Boyacense", "Colombiana"],
            price_level=2,
            features=["wifi", "parking", "outdoor_seating"],
        )

        # Assert
        assert restaurant_data.name == "La Casona Boyacense"
        assert restaurant_data.description == "Restaurante típico de comida boyacense"
        assert restaurant_data.postal_code == "150001"
        assert restaurant_data.email == "lacasona@example.com"
        assert str(restaurant_data.website) == "https://lacasona.com/"
        # GeoLocation uses Decimal for precision
        assert float(restaurant_data.location.latitude) == 5.5353
        assert float(restaurant_data.location.longitude) == -73.3678
        assert len(restaurant_data.cuisine_types) == 2
        assert restaurant_data.price_level == 2
        assert "wifi" in restaurant_data.features

    def test_create_restaurant_data_with_invalid_name_empty(self):
        """Test creating restaurant with empty name raises validation error.

        Given: Restaurant data with empty name
        When: Creating RestaurantData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RestaurantData(
                name="",  # ❌ Empty name
                address="Calle 1",
                city="Tunja",
                phone="+57 300 123 4567",
            )

        assert "name" in str(exc_info.value)

    def test_create_restaurant_data_with_invalid_website_url(self):
        """Test creating restaurant with invalid URL raises validation error.

        Given: Restaurant data with invalid website URL
        When: Creating RestaurantData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RestaurantData(
                name="Test",
                address="Calle 1",
                city="Tunja",
                phone="+57 300 123 4567",
                website="not-a-valid-url",  # ❌ Invalid URL
            )

        assert "website" in str(exc_info.value)

    def test_create_restaurant_data_with_invalid_price_level_too_high(self):
        """Test creating restaurant with price level > 4 raises error.

        Given: Restaurant data with price_level = 5 (max is 4)
        When: Creating RestaurantData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RestaurantData(
                name="Test",
                address="Calle 1",
                city="Tunja",
                phone="+57 300 123 4567",
                price_level=5,  # ❌ Max is 4
            )

        assert "price_level" in str(exc_info.value)

    def test_create_restaurant_data_with_invalid_price_level_too_low(self):
        """Test creating restaurant with price level < 1 raises error.

        Given: Restaurant data with price_level = 0 (min is 1)
        When: Creating RestaurantData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            RestaurantData(
                name="Test",
                address="Calle 1",
                city="Tunja",
                phone="+57 300 123 4567",
                price_level=0,  # ❌ Min is 1
            )

        assert "price_level" in str(exc_info.value)


class TestRestaurant:
    """Unit tests for Restaurant entity (with audit fields)."""

    def test_create_restaurant_entity_with_all_fields(self):
        """Test creating complete Restaurant entity with audit fields.

        Given: Complete restaurant data including ID and timestamps
        When: Creating Restaurant entity
        Then: All fields including audit fields are set correctly
        """
        # Arrange
        now = datetime.now(UTC)
        restaurant_id = "01K8E0Z3SRNDMSZPN91V7A64T3"
        creator_id = "01K8E0CREATOR123456789ABC"

        # Act
        restaurant = Restaurant(
            # Audit fields
            id=restaurant_id,
            created_at=now,
            updated_at=now,
            created_by=creator_id,
            updated_by=creator_id,
            # Restaurant data
            name="Test Restaurant",
            address="Calle 1 #2-3",
            city="Tunja",
            phone="+57 300 123 4567",
            cuisine_types=["Colombiana"],
            features=["wifi"],
        )

        # Assert
        # Audit fields
        assert restaurant.id == restaurant_id
        assert restaurant.created_at == now
        assert restaurant.updated_at == now
        assert restaurant.created_by == creator_id
        assert restaurant.updated_by == creator_id
        # Restaurant data
        assert restaurant.name == "Test Restaurant"
        assert restaurant.city == "Tunja"

    def test_restaurant_model_dump_mode_json_converts_http_url(self):
        """Test that model_dump(mode='json') converts HttpUrl to string.

        Given: Restaurant with HttpUrl website
        When: Calling restaurant.model_dump(mode='json')
        Then: website field is converted to string
        """
        # Arrange
        restaurant = Restaurant(
            id="01K8E0Z3SRNDMSZPN91V7A64T3",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            name="Test",
            address="Calle 1",
            city="Tunja",
            phone="+57 300 123 4567",
            website=HttpUrl("https://example.com"),
            cuisine_types=[],
            features=[],
        )

        # Act
        dumped = restaurant.model_dump(mode="json")

        # Assert
        assert isinstance(dumped["website"], str)
        assert dumped["website"] == "https://example.com/"

    def test_restaurant_validates_from_attributes(self):
        """Test that Restaurant can be validated from ORM model attributes.

        Given: Dictionary with restaurant attributes (simulating ORM)
        When: Using model_validate() with from_attributes config
        Then: Restaurant entity is created successfully
        """
        # Arrange
        orm_data = {
            "id": "01K8E0Z3SRNDMSZPN91V7A64T3",
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "name": "ORM Restaurant",
            "address": "Calle 1",
            "city": "Tunja",
            "phone": "+57 300 123 4567",
            "cuisine_types": ["Colombiana"],
            "features": ["wifi"],
            "state": "Boyacá",
            "country": "Colombia",
        }

        # Act
        restaurant = Restaurant.model_validate(orm_data)

        # Assert
        assert restaurant.name == "ORM Restaurant"
        assert restaurant.city == "Tunja"
