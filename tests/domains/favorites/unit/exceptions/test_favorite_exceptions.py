"""Unit tests for favorites domain exceptions."""

from app.domains.favorites.domain.exceptions import (
    FavoriteAlreadyExistsError,
    FavoriteNotFoundError,
)


class TestFavoriteExceptions:
    """Tests for custom favorites exceptions."""

    def test_favorite_already_exists_error_fields(self) -> None:
        """FavoriteAlreadyExistsError should expose context and message."""
        exc = FavoriteAlreadyExistsError(
            user_id="01ABCDEFALREADYEXISTSUSERID",
            entity_type="restaurant",
            entity_id="01ABCDEFALREADYEXISTSENTITY",
        )
        assert "ALREADY_EXISTS" in exc.error_code
        assert "Favorite" in exc.message
        assert exc.context["identifier"].startswith("01ABCDEFALREADYEXISTSUSERID")

    def test_favorite_not_found_error_fields(self) -> None:
        """FavoriteNotFoundError should expose context and message."""
        exc = FavoriteNotFoundError(
            user_id="01NOTFOUNDUSER",
            entity_type="dish",
            entity_id="01NOTFOUNDENTITY",
        )
        assert exc.error_code == "FAVORITE_NOT_FOUND"
        assert "not found" in exc.message.lower()
        assert exc.context["entity_id"].endswith(":dish:01NOTFOUNDENTITY")
