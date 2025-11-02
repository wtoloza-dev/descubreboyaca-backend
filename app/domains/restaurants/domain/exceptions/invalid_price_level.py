"""Invalid price level domain exception."""

from typing import Any

from app.shared.domain.exceptions import ValidationException


class InvalidPriceLevelException(ValidationException):
    """Exception raised when an invalid price level is provided.

    This exception is raised when attempting to set a price level
    that is not recognized by the system (must be 1-4).

    Example:
        >>> raise InvalidPriceLevelException(
        ...     price_level="INVALID",
        ... )
    """

    def __init__(
        self,
        price_level: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize invalid price level exception.

        Args:
            price_level: The invalid price level value
            context: Additional context
        """
        full_context = {
            "price_level": price_level,
            "field": "price_level",
            "valid_range": "1-4",
            **(context or {}),
        }
        super().__init__(
            message=f"Invalid price level: '{price_level}'",
            context=full_context,
            error_code="INVALID_PRICE_LEVEL",
        )
