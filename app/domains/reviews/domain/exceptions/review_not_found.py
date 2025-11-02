"""Review not found exception.

This module defines the exception raised when a review is not found.
"""

from app.shared.domain.exceptions import DomainException


class ReviewNotFoundException(DomainException):
    """Exception raised when a review is not found.

    This exception is raised when attempting to retrieve, update, or delete
    a review that does not exist in the system.

    Attributes:
        review_id: The ULID of the review that was not found
    """

    def __init__(self, review_id: str) -> None:
        """Initialize the exception.

        Args:
            review_id: The ULID of the review that was not found
        """
        super().__init__(
            error_code="REVIEW_NOT_FOUND",
            message=f"Review with ID '{review_id}' was not found",
            context={"review_id": review_id},
        )
