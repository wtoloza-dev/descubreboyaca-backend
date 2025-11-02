"""Invalid rating exception.

This module defines the exception raised when an invalid rating is provided.
"""

from app.shared.domain.exceptions import DomainException


class InvalidRatingException(DomainException):
    """Exception raised when an invalid rating is provided.

    This exception is raised when a rating value is not within the valid
    range of 1 to 5 stars.

    Attributes:
        rating: The invalid rating value provided
    """

    def __init__(self, rating: int) -> None:
        """Initialize the exception.

        Args:
            rating: The invalid rating value provided
        """
        super().__init__(
            error_code="INVALID_RATING",
            message=f"Rating must be between 1 and 5 stars, got {rating}",
            context={"rating": rating, "valid_range": "1-5"},
        )
