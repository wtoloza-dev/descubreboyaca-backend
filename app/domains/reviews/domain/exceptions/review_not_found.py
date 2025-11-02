"""Review not found domain exception."""

from typing import Any

from app.shared.domain.exceptions import NotFoundException


class ReviewNotFoundException(NotFoundException):
    """Exception raised when a review is not found.

    This exception is raised when attempting to retrieve, update, or delete
    a review that does not exist in the system.

    Example:
        >>> raise ReviewNotFoundException(
        ...     review_id="01HQ123ABC",
        ... )
    """

    def __init__(
        self,
        review_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize review not found exception.

        Args:
            review_id: ULID of the review that was not found
            context: Additional context
        """
        full_context = {
            "review_id": review_id,
            **(context or {}),
        }
        super().__init__(
            message=f"Review with ID '{review_id}' not found",
            context=full_context,
            error_code="REVIEW_NOT_FOUND",
        )
