"""Expired token exception.

This module defines the exception raised when a JWT token has expired.
"""

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class ExpiredTokenException(AuthenticationException):
    """Exception raised when a JWT token has expired.

    Raised when attempting to use an expired token.
    """

    def __init__(self, message: str = "Authentication token has expired") -> None:
        """Initialize expired token exception.

        Args:
            message: Error message
        """
        super().__init__(
            error_code="EXPIRED_TOKEN",
            message=message,
        )
