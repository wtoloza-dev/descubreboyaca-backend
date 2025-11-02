"""Cannot remove primary owner domain exception."""

from typing import Any

from app.shared.domain.exceptions import ValidationException


class CannotRemovePrimaryOwnerException(ValidationException):
    """Exception raised when attempting to remove the primary owner.

    This exception is raised when trying to remove a primary owner
    without transferring ownership first.

    Example:
        >>> raise CannotRemovePrimaryOwnerException(
        ...     owner_id="01HQ123ABC",
        ...     restaurant_id="01HQ456DEF",
        ... )
    """

    def __init__(
        self,
        owner_id: str,
        restaurant_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize cannot remove primary owner exception.

        Args:
            owner_id: ULID of the primary owner being removed
            restaurant_id: Optional ULID of the restaurant
            context: Additional context
        """
        full_context = {
            "owner_id": owner_id,
            "field": "is_primary",
            **({"restaurant_id": restaurant_id} if restaurant_id else {}),
            **(context or {}),
        }
        super().__init__(
            message="Cannot remove primary owner. Transfer ownership first or assign a new primary owner.",
            context=full_context,
            error_code="CANNOT_REMOVE_PRIMARY_OWNER",
        )
