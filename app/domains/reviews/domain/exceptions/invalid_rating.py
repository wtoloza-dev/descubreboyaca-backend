"""Invalid rating domain exception."""

from typing import Any

from app.shared.domain.exceptions import ValidationException


class InvalidRatingException(ValidationException):
    """Exception raised when an invalid rating is provided.

    This exception is raised when a rating value is not within the valid
    range of 1 to 5 stars.

    Example:
        >>> raise InvalidRatingException(rating=6)
    """

    def __init__(
        self,
        rating: int,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize invalid rating exception.

        Args:
            rating: The invalid rating value provided
            context: Additional context
        """
        full_context = {
            "rating": rating,
            "valid_range": "1-5",
            **(context or {}),
        }
        super().__init__(
            message=f"Rating must be between 1 and 5 stars, got {rating}",
            context=full_context,
            error_code="INVALID_RATING",
        )
