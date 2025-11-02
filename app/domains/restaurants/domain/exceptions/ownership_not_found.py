"""Ownership not found domain exception."""

from typing import Any

from app.shared.domain.exceptions import NotFoundException


class OwnershipNotFoundException(NotFoundException):
    """Exception raised when an ownership relationship is not found.

    This exception is raised when attempting to access an ownership
    relationship that doesn't exist in the system.

    Example:
        >>> raise OwnershipNotFoundException(
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
        """Initialize ownership not found exception.

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
            message=f"Ownership relationship not found for restaurant '{restaurant_id}' and owner '{owner_id}'",
            context=full_context,
            error_code="OWNERSHIP_NOT_FOUND",
        )
