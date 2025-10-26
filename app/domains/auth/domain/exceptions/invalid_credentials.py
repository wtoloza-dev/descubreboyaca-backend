"""Invalid credentials exception.

This module defines the exception raised when user credentials are invalid.
"""

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class InvalidCredentialsException(AuthenticationException):
    """Exception raised when user credentials are invalid.

    Raised when email/password combination doesn't match.
    """

    def __init__(self, message: str = "Invalid email or password") -> None:
        """Initialize invalid credentials exception.

        Args:
            message: Error message
        """
        super().__init__(
            error_code="INVALID_CREDENTIALS",
            message=message,
        )
