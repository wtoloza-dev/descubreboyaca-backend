"""Unit tests for Favorite and FavoriteData entities.

Given-When-Then style docstrings and AAA comments per testing architecture.
"""

from datetime import UTC

from ulid import ULID

from app.domains.favorites.domain.entities import Favorite, FavoriteData
from app.domains.favorites.domain.enums import EntityType


class TestFavoriteEntity:
    """Unit tests for Favorite entity behavior."""

    def test_create_favorite_entity_generates_id_and_created_at(self) -> None:
        """Favorite should auto-generate ULID id and UTC created_at.

        Given: Valid FavoriteData
        When: Creating Favorite from data
        Then: Entity has 26-char ULID id and UTC-aware created_at
        """
        # Arrange
        data = FavoriteData(
            user_id=str(ULID()),
            entity_type=EntityType.RESTAURANT,
            entity_id=str(ULID()),
        )

        # Act
        favorite = Favorite(**data.model_dump())

        # Assert
        assert isinstance(favorite.id, str)
        assert len(favorite.id) == 26  # ULID length
        assert favorite.created_at.tzinfo is UTC

    def test_favorite_data_accepts_valid_input(self) -> None:
        """FavoriteData should accept valid ULIDs and entity type.

        Given: Valid ULID strings and EntityType
        When: Building FavoriteData
        Then: Fields are stored as provided
        """
        # Arrange
        user_id = str(ULID())
        entity_id = str(ULID())

        # Act
        data = FavoriteData(
            user_id=user_id,
            entity_type=EntityType.DISH,
            entity_id=entity_id,
        )

        # Assert
        assert data.user_id == user_id
        assert data.entity_type is EntityType.DISH
        assert data.entity_id == entity_id
