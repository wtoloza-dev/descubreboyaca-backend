"""Forbidden exception.

This module defines the base exception for permission/authorization errors.
"""

from typing import Any

from app.shared.domain.exceptions.domain_exception import DomainException


class ForbiddenException(DomainException):
    """Exception raised when user lacks permission to perform an action.

    This is a base exception for all permission-denied scenarios across domains.
    Specific domain exceptions should inherit from this class.

    Example:
        >>> raise ForbiddenException(
        ...     message="Insufficient permissions to delete restaurant '123'",
        ...     context={"restaurant_id": "123", "required_role": "owner"},
        ...     error_code="INSUFFICIENT_PERMISSIONS",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "FORBIDDEN",
    ) -> None:
        """Initialize forbidden exception.

        Args:
            message: Human-readable error message
            context: Additional context about the error
            error_code: Machine-readable error code
        """
        super().__init__(
            message=message,
            context=context,
            error_code=error_code,
        )

