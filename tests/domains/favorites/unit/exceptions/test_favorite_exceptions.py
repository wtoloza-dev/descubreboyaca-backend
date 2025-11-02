"""Unit tests for favorites domain exceptions."""

from app.domains.favorites.domain.exceptions import (
    FavoriteAlreadyExistsException,
    FavoriteNotFoundException,
)


class TestFavoriteExceptions:
    """Tests for custom favorites exceptions."""

    def test_favorite_already_exists_exception_fields(self) -> None:
        """FavoriteAlreadyExistsException should expose context and message."""
        exc = FavoriteAlreadyExistsException(
            user_id="01ABCDEFALREADYEXISTSUSERID",
            entity_type="restaurant",
            entity_id="01ABCDEFALREADYEXISTSENTITY",
        )
        assert exc.error_code == "FAVORITE_ALREADY_EXISTS"
        assert "already favorited" in exc.message.lower()
        assert exc.context["user_id"] == "01ABCDEFALREADYEXISTSUSERID"
        assert exc.context["entity_type"] == "restaurant"
        assert exc.context["entity_id"] == "01ABCDEFALREADYEXISTSENTITY"

    def test_favorite_not_found_exception_fields(self) -> None:
        """FavoriteNotFoundException should expose context and message."""
        exc = FavoriteNotFoundException(
            user_id="01NOTFOUNDUSER",
            entity_type="dish",
            entity_id="01NOTFOUNDENTITY",
        )
        assert exc.error_code == "FAVORITE_NOT_FOUND"
        assert "not found" in exc.message.lower()
        assert exc.context["user_id"] == "01NOTFOUNDUSER"
        assert exc.context["entity_type"] == "dish"
        assert exc.context["entity_id"] == "01NOTFOUNDENTITY"
