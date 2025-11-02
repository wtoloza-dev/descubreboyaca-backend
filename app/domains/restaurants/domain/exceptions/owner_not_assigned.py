"""Owner not assigned domain exception."""

from typing import Any

from app.shared.domain.exceptions import ValidationException


class OwnerNotAssignedException(ValidationException):
    """Exception raised when attempting to transfer ownership to an unassigned user.

    This exception is raised when trying to make someone primary owner
    who is not yet assigned to the restaurant.

    Example:
        >>> raise OwnerNotAssignedException(
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
        """Initialize owner not assigned exception.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner
            context: Additional context
        """
        full_context = {
            "restaurant_id": restaurant_id,
            "owner_id": owner_id,
            "field": "owner_id",
            **(context or {}),
        }
        super().__init__(
            message=f"Owner '{owner_id}' must be assigned to restaurant '{restaurant_id}' before transferring ownership",
            context=full_context,
            error_code="OWNER_NOT_ASSIGNED",
        )
