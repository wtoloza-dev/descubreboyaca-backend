"""Entity not found exception.

This module defines the exception raised when the entity being reviewed
does not exist.
"""

from app.shared.domain.exceptions import DomainException


class EntityNotFoundException(DomainException):
    """Exception raised when the entity being reviewed does not exist.

    This exception is raised when a user attempts to create a review for
    an entity (restaurant, event, place) that does not exist in the system.

    Attributes:
        entity_type: The type of entity that was not found
        entity_id: The ULID of the entity that was not found
    """

    def __init__(self, entity_type: str, entity_id: str) -> None:
        """Initialize the exception.

        Args:
            entity_type: The type of entity that was not found
            entity_id: The ULID of the entity that was not found
        """
        super().__init__(
            error_code="ENTITY_NOT_FOUND",
            message=f"{entity_type.capitalize()} with ID '{entity_id}' was not found",
            context={
                "entity_type": entity_type,
                "entity_id": entity_id,
            },
        )
