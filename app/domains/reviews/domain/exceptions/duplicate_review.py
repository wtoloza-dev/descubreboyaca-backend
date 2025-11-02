"""Duplicate review exception.

This module defines the exception raised when a user tries to create
a duplicate review for the same entity.
"""

from app.shared.domain.exceptions import DomainException


class DuplicateReviewException(DomainException):
    """Exception raised when a user tries to create a duplicate review.

    This exception is raised when a user attempts to create a second review
    for an entity they have already reviewed. Each user can only have one
    review per entity.

    Attributes:
        user_id: The ULID of the user attempting to create the duplicate review
        entity_type: The type of entity being reviewed
        entity_id: The ULID of the entity being reviewed
    """

    def __init__(self, user_id: str, entity_type: str, entity_id: str) -> None:
        """Initialize the exception.

        Args:
            user_id: The ULID of the user attempting to create the duplicate review
            entity_type: The type of entity being reviewed
            entity_id: The ULID of the entity being reviewed
        """
        super().__init__(
            error_code="DUPLICATE_REVIEW",
            message=(
                f"User '{user_id}' has already reviewed {entity_type} '{entity_id}'. "
                "Only one review per entity is allowed."
            ),
            context={
                "user_id": user_id,
                "entity_type": entity_type,
                "entity_id": entity_id,
            },
        )
