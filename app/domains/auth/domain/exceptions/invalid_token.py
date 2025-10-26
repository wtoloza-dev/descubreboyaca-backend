"""Invalid token exception.

This module defines the exception raised when a JWT token is invalid.
"""

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class InvalidTokenException(AuthenticationException):
    """Exception raised when a JWT token is invalid.

    Raised when token signature is invalid or token is malformed.
    """

    def __init__(self, message: str = "Invalid authentication token") -> None:
        """Initialize invalid token exception.

        Args:
            message: Error message
        """
        super().__init__(
            error_code="INVALID_TOKEN",
            message=message,
        )
