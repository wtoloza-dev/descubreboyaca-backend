"""User inactive exception.

This module defines the exception raised when attempting to authenticate an inactive user.
"""

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class UserInactiveException(AuthenticationException):
    """Exception raised when attempting to authenticate an inactive user.

    Raised when user account has been deactivated.
    """

    def __init__(self, email: str) -> None:
        """Initialize user inactive exception.

        Args:
            email: Email of the inactive user
        """
        super().__init__(
            error_code="USER_INACTIVE",
            message=f"User account '{email}' is inactive",
            context={"email": email},
        )
        self.email = email
