"""Favorite not found domain exception."""

from typing import Any

from app.shared.domain.exceptions import NotFoundException


class FavoriteNotFoundException(NotFoundException):
    """Exception raised when a favorite is not found.

    This exception is raised when attempting to access or delete a favorite
    that doesn't exist for the given user and entity.

    Example:
        >>> raise FavoriteNotFoundException(
        ...     user_id="01HQ123ABC",
        ...     entity_type="Restaurant",
        ...     entity_id="01HQ456DEF",
        ... )
    """

    def __init__(
        self,
        user_id: str,
        entity_type: str,
        entity_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize favorite not found exception.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity (e.g., Restaurant)
            entity_id: ULID of the entity
            context: Additional context
        """
        full_context = {
            "user_id": user_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            **(context or {}),
        }
        super().__init__(
            message=f"Favorite not found for user '{user_id}', {entity_type} '{entity_id}'",
            context=full_context,
            error_code="FAVORITE_NOT_FOUND",
        )

