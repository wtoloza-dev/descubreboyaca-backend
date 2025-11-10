"""Missing header domain exception."""

from typing import Any

from app.shared.domain.exceptions.validation import ValidationException


class MissingHeaderException(ValidationException):
    """Exception raised when a required HTTP header is missing.

    This exception is raised when a request is missing a required header
    for proper operation (e.g., user context headers).

    Example:
        >>> raise MissingHeaderException(header_name="X-User-ID")
    """

    def __init__(
        self,
        header_name: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize missing header exception.

        Args:
            header_name: Name of the required header that is missing
            context: Additional context
        """
        full_context = {
            "header_name": header_name,
            **(context or {}),
        }
        super().__init__(
            message=f"Required header '{header_name}' is missing",
            context=full_context,
            error_code="MISSING_HEADER",
        )
