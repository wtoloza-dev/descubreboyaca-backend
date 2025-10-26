"""Invalid cuisine type exception.

This module defines the exception raised when an invalid cuisine type is provided.
"""

from app.shared.domain.exceptions.base import ValidationException


class InvalidCuisineTypeException(ValidationException):
    """Exception raised when an invalid cuisine type is provided.

    This exception is raised when attempting to set a cuisine type
    that is not recognized by the system.

    Example:
        >>> raise InvalidCuisineTypeException("INVALID_TYPE")
        InvalidCuisineTypeException: Invalid cuisine type: 'INVALID_TYPE'
    """

    def __init__(self, cuisine_type: str) -> None:
        """Initialize invalid cuisine type exception.

        Args:
            cuisine_type: The invalid cuisine type value
        """
        super().__init__(
            message=f"Invalid cuisine type: '{cuisine_type}'",
            field="cuisine_type",
            value=cuisine_type,
        )
