"""User already exists exception.

This module defines the exception raised when attempting to create a user that already exists.
"""

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class UserAlreadyExistsException(AuthenticationException):
    """Exception raised when attempting to create a user that already exists.

    Raised when registering with an email that's already in use.
    """

    def __init__(self, email: str) -> None:
        """Initialize user already exists exception.

        Args:
            email: Email address that already exists
        """
        super().__init__(
            error_code="USER_ALREADY_EXISTS",
            message=f"User with email '{email}' already exists",
            context={"email": email},
        )
        self.email = email
