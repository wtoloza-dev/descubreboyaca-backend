"""Unauthorized review exception.

This module defines the exception raised when a user attempts to modify
or delete a review they do not own.
"""

from app.shared.domain.exceptions import DomainException


class UnauthorizedReviewException(DomainException):
    """Exception raised when a user attempts unauthorized review operations.

    This exception is raised when a user tries to update or delete a review
    that does not belong to them. Only the review owner can modify their
    own reviews.

    Attributes:
        user_id: The ULID of the user attempting the unauthorized operation
        review_id: The ULID of the review they attempted to modify
    """

    def __init__(self, user_id: str, review_id: str) -> None:
        """Initialize the exception.

        Args:
            user_id: The ULID of the user attempting the unauthorized operation
            review_id: The ULID of the review they attempted to modify
        """
        super().__init__(
            error_code="UNAUTHORIZED_REVIEW_OPERATION",
            message=(
                f"User '{user_id}' is not authorized to modify review '{review_id}'. "
                "Only the review owner can modify their reviews."
            ),
            context={
                "user_id": user_id,
                "review_id": review_id,
            },
        )
