"""Not found exception.

This module defines the base exception for resource not found errors.
"""

from typing import Any

from app.shared.domain.exceptions.domain_exception import DomainException


class NotFoundException(DomainException):
    """Exception raised when a requested resource doesn't exist.

    This is a base exception for all not-found scenarios across domains.
    Specific domain exceptions should inherit from this class.

    Example:
        >>> raise NotFoundException(
        ...     message="User with ID '123' not found",
        ...     context={"user_id": "123"},
        ...     error_code="USER_NOT_FOUND",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "NOT_FOUND",
    ) -> None:
        """Initialize not found exception.

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

