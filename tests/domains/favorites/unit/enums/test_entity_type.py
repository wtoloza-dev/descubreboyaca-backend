"""Unit tests for EntityType StrEnum.

Ensures string behavior and allowed values.
"""

from app.domains.favorites.domain.enums import EntityType


class TestEntityType:
    """Tests for EntityType string enum behavior."""

    def test_values_are_strings(self) -> None:
        """Each enum member should be a string and equal to its name value."""
        assert isinstance(EntityType.RESTAURANT, str)
        assert isinstance(EntityType.DISH, str)
        assert str(EntityType.EVENT) == "event"

    def test_membership(self) -> None:
        """Enum contains expected members."""
        assert EntityType.RESTAURANT.value == "restaurant"
        assert EntityType.DISH.value == "dish"
        assert EntityType.PLACE.value == "place"
        assert EntityType.ACTIVITY.value == "activity"
