"""Missing header exception.

This module defines exceptions for missing required headers in HTTP requests.
"""

from app.shared.domain.exceptions.base import DomainException


class MissingHeaderException(DomainException):
    """Exception raised when a required HTTP header is missing.

    This exception is raised when a request is missing a required header.

    Attributes:
        header_name: The name of the missing header.
    """

    def __init__(self, header_name: str) -> None:
        """Initialize missing header exception.

        Args:
            header_name: Name of the required header that is missing
        """
        super().__init__(
            error_code="MISSING_HEADER",
            message=f"Required header '{header_name}' is missing",
            context={"header_name": header_name},
        )
        self.header_name = header_name

