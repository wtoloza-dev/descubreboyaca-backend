"""Ownership already exists domain exception."""

from typing import Any

from app.shared.domain.exceptions import AlreadyExistsException


class OwnershipAlreadyExistsException(AlreadyExistsException):
    """Exception raised when attempting to create a duplicate ownership relationship.

    This exception is raised when an owner is already assigned to a restaurant.

    Example:
        >>> raise OwnershipAlreadyExistsException(
        ...     restaurant_id="01HQ123ABC",
        ...     owner_id="01HQ456DEF",
        ... )
    """

    def __init__(
        self,
        restaurant_id: str,
        owner_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ownership already exists exception.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner
            context: Additional context
        """
        full_context = {
            "restaurant_id": restaurant_id,
            "owner_id": owner_id,
            **(context or {}),
        }
        super().__init__(
            message=f"Owner '{owner_id}' is already assigned to restaurant '{restaurant_id}'",
            context=full_context,
            error_code="OWNERSHIP_ALREADY_EXISTS",
        )
