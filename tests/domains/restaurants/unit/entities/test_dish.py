"""Unit tests for Dish entity validation.

This module tests the validation rules and behavior of DishData and Dish entities.
"""

from decimal import Decimal

import pytest
from pydantic import HttpUrl, ValidationError

from app.domains.restaurants.domain import Dish, DishData


class TestDishData:
    """Unit tests for DishData validation."""

    def test_create_dish_data_with_valid_minimal_data(self):
        """Test creating dish data with valid minimal required fields.

        Given: Valid minimal dish data (name, category, price)
        When: Creating DishData instance
        Then: Instance is created successfully with default values
        """
        # Arrange & Act
        dish_data = DishData(
            name="Ajiaco",
            category="main_course",
            price=Decimal("25000.00"),
        )

        # Assert
        assert dish_data.name == "Ajiaco"
        assert dish_data.category == "main_course"
        assert dish_data.price == Decimal("25000.00")
        assert dish_data.description is None
        assert dish_data.is_available is True  # Default
        assert dish_data.is_featured is False  # Default
        assert dish_data.display_order == 0  # Default
        assert dish_data.dietary_restrictions == []  # Default
        assert dish_data.ingredients == []  # Default
        assert dish_data.allergens == []  # Default
        assert dish_data.flavor_profile == {}  # Default

    def test_create_dish_data_with_full_data(self):
        """Test creating dish data with all fields populated.

        Given: Complete dish data with all optional fields
        When: Creating DishData instance
        Then: Instance is created with all values set correctly
        """
        # Arrange & Act
        dish_data = DishData(
            name="Bandeja Paisa",
            description="Traditional Colombian platter",
            category="main_course",
            price=Decimal("35000.00"),
            original_price=Decimal("40000.00"),
            is_available=True,
            preparation_time_minutes=60,
            serves=1,
            calories=1200,
            image_url="https://example.com/bandeja.jpg",
            dietary_restrictions=["gluten_free"],
            ingredients=["beans", "rice", "meat"],
            allergens=["egg"],
            flavor_profile={"savory": "high", "hearty": "extreme"},
            is_featured=True,
            display_order=1,
        )

        # Assert
        assert dish_data.name == "Bandeja Paisa"
        assert dish_data.description == "Traditional Colombian platter"
        assert dish_data.price == Decimal("35000.00")
        assert dish_data.original_price == Decimal("40000.00")
        assert dish_data.preparation_time_minutes == 60
        assert dish_data.serves == 1
        assert dish_data.calories == 1200
        assert str(dish_data.image_url) == "https://example.com/bandeja.jpg"
        assert dish_data.dietary_restrictions == ["gluten_free"]
        assert dish_data.ingredients == ["beans", "rice", "meat"]
        assert dish_data.allergens == ["egg"]
        assert dish_data.flavor_profile == {"savory": "high", "hearty": "extreme"}
        assert dish_data.is_featured is True
        assert dish_data.display_order == 1

    def test_create_dish_data_with_invalid_name_empty(self):
        """Test creating dish data with empty name fails validation.

        Given: Dish data with empty name
        When: Creating DishData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DishData(
                name="",  # Invalid: empty name
                category="dessert",
                price=Decimal("8000.00"),
            )

        # Assert error mentions name field
        assert "name" in str(exc_info.value)

    def test_create_dish_data_with_invalid_name_too_long(self):
        """Test creating dish data with name exceeding max length fails.

        Given: Dish data with name > 255 characters
        When: Creating DishData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DishData(
                name="A" * 256,  # Invalid: too long
                category="dessert",
                price=Decimal("8000.00"),
            )

        # Assert error mentions name field
        assert "name" in str(exc_info.value)

    def test_create_dish_data_with_invalid_category_empty(self):
        """Test creating dish data with empty category fails validation.

        Given: Dish data with empty category
        When: Creating DishData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DishData(
                name="Test Dish",
                category="",  # Invalid: empty category
                price=Decimal("8000.00"),
            )

        # Assert error mentions category field
        assert "category" in str(exc_info.value)

    def test_create_dish_data_with_invalid_price_negative(self):
        """Test creating dish data with negative price fails validation.

        Given: Dish data with negative price
        When: Creating DishData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DishData(
                name="Test Dish",
                category="dessert",
                price=Decimal("-1000.00"),  # Invalid: negative
            )

        # Assert error mentions price field
        assert "price" in str(exc_info.value)

    def test_create_dish_data_with_invalid_preparation_time_negative(self):
        """Test creating dish data with negative preparation time fails.

        Given: Dish data with negative preparation_time_minutes
        When: Creating DishData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DishData(
                name="Test Dish",
                category="dessert",
                price=Decimal("8000.00"),
                preparation_time_minutes=-10,  # Invalid: negative
            )

        # Assert error mentions preparation_time_minutes field
        assert "preparation_time_minutes" in str(exc_info.value)

    def test_create_dish_data_with_invalid_preparation_time_too_large(self):
        """Test creating dish data with preparation time exceeding max fails.

        Given: Dish data with preparation_time_minutes > 600
        When: Creating DishData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DishData(
                name="Test Dish",
                category="dessert",
                price=Decimal("8000.00"),
                preparation_time_minutes=700,  # Invalid: > 600
            )

        # Assert error mentions preparation_time_minutes field
        assert "preparation_time_minutes" in str(exc_info.value)

    def test_create_dish_data_with_invalid_serves_zero(self):
        """Test creating dish data with serves=0 fails validation.

        Given: Dish data with serves=0
        When: Creating DishData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DishData(
                name="Test Dish",
                category="dessert",
                price=Decimal("8000.00"),
                serves=0,  # Invalid: must be >= 1
            )

        # Assert error mentions serves field
        assert "serves" in str(exc_info.value)

    def test_create_dish_data_with_invalid_calories_negative(self):
        """Test creating dish data with negative calories fails validation.

        Given: Dish data with negative calories
        When: Creating DishData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DishData(
                name="Test Dish",
                category="dessert",
                price=Decimal("8000.00"),
                calories=-100,  # Invalid: negative
            )

        # Assert error mentions calories field
        assert "calories" in str(exc_info.value)

    def test_create_dish_data_with_invalid_display_order_negative(self):
        """Test creating dish data with negative display_order fails.

        Given: Dish data with negative display_order
        When: Creating DishData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DishData(
                name="Test Dish",
                category="dessert",
                price=Decimal("8000.00"),
                display_order=-1,  # Invalid: negative
            )

        # Assert error mentions display_order field
        assert "display_order" in str(exc_info.value)

    def test_create_dish_data_with_invalid_image_url(self):
        """Test creating dish data with invalid URL format fails.

        Given: Dish data with malformed URL
        When: Creating DishData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DishData(
                name="Test Dish",
                category="dessert",
                price=Decimal("8000.00"),
                image_url="not-a-valid-url",  # Invalid: not a URL
            )

        # Assert error mentions image_url field
        assert "image_url" in str(exc_info.value)


class TestDish:
    """Unit tests for Dish entity."""

    def test_create_dish_with_all_fields(self):
        """Test creating complete Dish entity with all fields.

        Given: Complete dish data with ID, restaurant_id, and audit fields
        When: Creating Dish instance
        Then: Instance is created with all fields set
        """
        # Arrange
        from datetime import UTC, datetime

        from app.shared.domain.factories import generate_ulid

        # Act
        dish = Dish(
            id=generate_ulid(),
            restaurant_id=generate_ulid(),
            name="Ajiaco",
            category="main_course",
            price=Decimal("25000.00"),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        # Assert
        assert dish.id is not None
        assert dish.restaurant_id is not None
        assert dish.name == "Ajiaco"
        assert dish.created_at is not None

    def test_dish_model_dump_mode_json_converts_http_url(self):
        """Test that HttpUrl fields convert to strings in JSON mode.

        Given: Dish entity with HttpUrl image_url
        When: Calling model_dump(mode="json")
        Then: image_url is serialized as string
        """
        # Arrange
        from datetime import UTC, datetime

        from app.shared.domain.factories import generate_ulid

        dish = Dish(
            id=generate_ulid(),
            restaurant_id=generate_ulid(),
            name="Ajiaco",
            category="main_course",
            price=Decimal("25000.00"),
            image_url=HttpUrl("https://example.com/dish.jpg"),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        # Act
        dumped = dish.model_dump(mode="json")

        # Assert
        assert isinstance(dumped["image_url"], str)
        assert dumped["image_url"] == "https://example.com/dish.jpg"

    def test_dish_model_dump_mode_json_converts_decimal_to_string(self):
        """Test that Decimal fields convert to strings in JSON mode.

        Given: Dish entity with Decimal price
        When: Calling model_dump(mode="json")
        Then: price is serialized as string
        """
        # Arrange
        from datetime import UTC, datetime

        from app.shared.domain.factories import generate_ulid

        dish = Dish(
            id=generate_ulid(),
            restaurant_id=generate_ulid(),
            name="Ajiaco",
            category="main_course",
            price=Decimal("25000.00"),
            original_price=Decimal("28000.00"),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        # Act
        dumped = dish.model_dump(mode="json")

        # Assert
        assert isinstance(dumped["price"], str)
        assert dumped["price"] == "25000.00"
        assert isinstance(dumped["original_price"], str)
        assert dumped["original_price"] == "28000.00"

    def test_dish_preserves_json_fields(self):
        """Test that JSON fields (lists and dicts) are preserved correctly.

        Given: Dish with dietary_restrictions, ingredients, allergens, and flavor_profile
        When: Creating and dumping Dish
        Then: All JSON fields are preserved with correct structure
        """
        # Arrange
        from datetime import UTC, datetime

        from app.shared.domain.factories import generate_ulid

        dish = Dish(
            id=generate_ulid(),
            restaurant_id=generate_ulid(),
            name="Bandeja Paisa",
            category="main_course",
            price=Decimal("35000.00"),
            dietary_restrictions=["gluten_free", "lactose_free"],
            ingredients=["beans", "rice", "meat", "egg"],
            allergens=["egg"],
            flavor_profile={"savory": "high", "hearty": "extreme", "spicy": "low"},
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        # Act
        dumped = dish.model_dump(mode="json")

        # Assert
        assert dumped["dietary_restrictions"] == ["gluten_free", "lactose_free"]
        assert dumped["ingredients"] == ["beans", "rice", "meat", "egg"]
        assert dumped["allergens"] == ["egg"]
        assert dumped["flavor_profile"] == {
            "savory": "high",
            "hearty": "extreme",
            "spicy": "low",
        }
