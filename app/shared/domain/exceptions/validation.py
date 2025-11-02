"""Validation exception.

This module defines the base exception for validation errors.
"""

from typing import Any

from app.shared.domain.exceptions.domain_exception import DomainException


class ValidationException(DomainException):
    """Exception raised when domain validation fails.

    This is a base exception for all validation errors across domains.
    Specific domain exceptions should inherit from this class.

    Example:
        >>> raise ValidationException(
        ...     message="Invalid email format 'notanemail'",
        ...     context={"field": "email", "value": "notanemail"},
        ...     error_code="INVALID_EMAIL_FORMAT",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "VALIDATION_ERROR",
    ) -> None:
        """Initialize validation exception.

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

