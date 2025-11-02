"""Invalid cuisine type domain exception."""

from typing import Any

from app.shared.domain.exceptions import ValidationException


class InvalidCuisineTypeException(ValidationException):
    """Exception raised when an invalid cuisine type is provided.

    This exception is raised when attempting to set a cuisine type
    that is not recognized by the system.

    Example:
        >>> raise InvalidCuisineTypeException(
        ...     cuisine_type="INVALID_TYPE",
        ... )
    """

    def __init__(
        self,
        cuisine_type: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize invalid cuisine type exception.

        Args:
            cuisine_type: The invalid cuisine type value
            context: Additional context
        """
        full_context = {
            "cuisine_type": cuisine_type,
            "field": "cuisine_type",
            **(context or {}),
        }
        super().__init__(
            message=f"Invalid cuisine type: '{cuisine_type}'",
            context=full_context,
            error_code="INVALID_CUISINE_TYPE",
        )
