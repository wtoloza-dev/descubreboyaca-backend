"""User not found exception.

This module defines the exception raised when a user is not found.
"""

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class UserNotFoundException(AuthenticationException):
    """Exception raised when a user is not found.

    Raised when attempting to access a user that doesn't exist.
    """

    def __init__(self, identifier: str) -> None:
        """Initialize user not found exception.

        Args:
            identifier: User identifier (email or ID) that was not found
        """
        super().__init__(
            error_code="USER_NOT_FOUND",
            message=f"User '{identifier}' not found",
            context={"identifier": identifier},
        )
        self.identifier = identifier
