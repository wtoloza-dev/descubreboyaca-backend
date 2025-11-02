"""Entity not found domain exception."""

from typing import Any

from app.shared.domain.exceptions import NotFoundException


class EntityNotFoundException(NotFoundException):
    """Exception raised when the entity being reviewed does not exist.

    This exception is raised when a user attempts to create a review for
    an entity (restaurant, event, place) that does not exist in the system.

    Example:
        >>> raise EntityNotFoundException(
        ...     entity_type="Restaurant",
        ...     entity_id="01HQ123ABC",
        ... )
    """

    def __init__(
        self,
        entity_type: str,
        entity_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize entity not found exception.

        Args:
            entity_type: Type of entity that was not found
            entity_id: ULID of the entity that was not found
            context: Additional context
        """
        full_context = {
            "entity_type": entity_type,
            "entity_id": entity_id,
            **(context or {}),
        }
        super().__init__(
            message=f"{entity_type.capitalize()} with ID '{entity_id}' not found",
            context=full_context,
            error_code=f"{entity_type.upper()}_NOT_FOUND",
        )
