"""Base domain exception.

This module defines the foundational exception class for all domain-level errors.
"""

from typing import Any


class DomainException(Exception):
    """Base exception for all domain-level errors.

    This exception serves as the foundation for all domain-specific exceptions.
    It provides a consistent structure with error_code, message, and context
    for error handling.

    All domain exceptions should inherit from this class or one of its subclasses.

    Attributes:
        error_code: A machine-readable error code identifying the exception type
        message: A human-readable error message describing the exception
        context: Additional contextual information about the error

    Example:
        >>> raise DomainException(
        ...     message="Business rule violation",
        ...     context={"rule": "max_items", "limit": 10},
        ...     error_code="BUSINESS_RULE_VIOLATION",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "DOMAIN_ERROR",
    ) -> None:
        """Initialize the domain exception.

        Args:
            message: A human-readable error message
            context: Optional dictionary with additional error context
            error_code: A machine-readable error code
        """
        self.error_code = error_code
        self.message = message
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of the exception.

        Returns:
            Formatted exception string with class name, error code, and message
        """
        return f"{self.__class__.__name__} [{self.error_code}]: {self.message}"
