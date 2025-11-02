"""Duplicate review domain exception."""

from typing import Any

from app.shared.domain.exceptions import AlreadyExistsException


class DuplicateReviewException(AlreadyExistsException):
    """Exception raised when a user tries to create a duplicate review.

    This exception is raised when a user attempts to create a second review
    for an entity they have already reviewed. Each user can only have one
    review per entity.

    Example:
        >>> raise DuplicateReviewException(
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
        """Initialize duplicate review exception.

        Args:
            user_id: ULID of the user attempting to create the duplicate review
            entity_type: Type of entity being reviewed
            entity_id: ULID of the entity being reviewed
            context: Additional context
        """
        full_context = {
            "user_id": user_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            **(context or {}),
        }
        super().__init__(
            message=f"User '{user_id}' has already reviewed {entity_type} '{entity_id}'",
            context=full_context,
            error_code="DUPLICATE_REVIEW",
        )
