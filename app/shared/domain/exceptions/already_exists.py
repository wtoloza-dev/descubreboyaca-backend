"""Already exists exception.

This module defines the base exception for duplicate resource errors.
"""

from typing import Any

from app.shared.domain.exceptions.domain_exception import DomainException


class AlreadyExistsException(DomainException):
    """Exception raised when attempting to create a duplicate resource.

    This is a base exception for all duplicate-entity scenarios across domains.
    Specific domain exceptions should inherit from this class.

    Example:
        >>> raise AlreadyExistsException(
        ...     message="User with email 'user@example.com' already exists",
        ...     context={"email": "user@example.com"},
        ...     error_code="USER_ALREADY_EXISTS",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "ALREADY_EXISTS",
    ) -> None:
        """Initialize already exists exception.

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

