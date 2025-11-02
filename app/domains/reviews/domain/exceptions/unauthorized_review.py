"""Unauthorized review domain exception."""

from typing import Any

from app.shared.domain.exceptions import ForbiddenException


class UnauthorizedReviewException(ForbiddenException):
    """Exception raised when a user attempts unauthorized review operations.

    This exception is raised when a user tries to update or delete a review
    that does not belong to them. Only the review owner can modify their
    own reviews.

    Example:
        >>> raise UnauthorizedReviewException(
        ...     user_id="01HQ123ABC",
        ...     review_id="01HQ456DEF",
        ... )
    """

    def __init__(
        self,
        user_id: str,
        review_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize unauthorized review exception.

        Args:
            user_id: ULID of the user attempting the unauthorized operation
            review_id: ULID of the review they attempted to modify
            context: Additional context
        """
        full_context = {
            "user_id": user_id,
            "review_id": review_id,
            **(context or {}),
        }
        super().__init__(
            message=f"User '{user_id}' is not authorized to modify review '{review_id}'",
            context=full_context,
            error_code="UNAUTHORIZED_REVIEW_OPERATION",
        )
