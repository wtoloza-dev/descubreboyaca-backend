"""Archive-specific domain exceptions.

This module defines exceptions specific to archive operations in the shared domain.
"""

from app.shared.domain.exceptions.base import DomainException


class AlreadyArchivedException(DomainException):
    """Exception raised when attempting to archive an already archived entity.

    This exception is raised when an archive operation is attempted on an entity
    that has already been archived.

    Attributes:
        entity_type: The type of entity that is already archived.
        entity_id: The identifier of the already archived entity.
    """

    def __init__(self, entity_type: str, entity_id: str) -> None:
        """Initialize already archived exception.

        Args:
            entity_type: Type of the entity that is already archived
            entity_id: Identifier of the already archived entity
        """
        super().__init__(
            error_code=f"{entity_type.upper()}_ALREADY_ARCHIVED",
            message=f"{entity_type} with ID '{entity_id}' is already archived",
            context={"entity_type": entity_type, "entity_id": entity_id},
        )
        self.entity_type = entity_type
        self.entity_id = entity_id
