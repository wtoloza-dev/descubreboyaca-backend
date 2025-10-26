"""Invalid price level exception.

This module defines the exception raised when an invalid price level is provided.
"""

from app.shared.domain.exceptions.base import ValidationException


class InvalidPriceLevelException(ValidationException):
    """Exception raised when an invalid price level is provided.

    This exception is raised when attempting to set a price level
    that is not recognized by the system.

    Example:
        >>> raise InvalidPriceLevelException("INVALID")
        InvalidPriceLevelException: Invalid price level: 'INVALID'
    """

    def __init__(self, price_level: str) -> None:
        """Initialize invalid price level exception.

        Args:
            price_level: The invalid price level value
        """
        super().__init__(
            message=f"Invalid price level: '{price_level}'",
            field="price_level",
            value=price_level,
        )
