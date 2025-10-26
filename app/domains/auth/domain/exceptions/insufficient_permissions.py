"""Insufficient permissions exception.

This module defines the exception raised when user lacks required permissions.
"""

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class InsufficientPermissionsException(AuthenticationException):
    """Exception raised when user lacks required permissions.

    Raised when user tries to access a resource they don't have permission for.
    """

    def __init__(self, required_role: str) -> None:
        """Initialize insufficient permissions exception.

        Args:
            required_role: Role required for the operation
        """
        super().__init__(
            error_code="INSUFFICIENT_PERMISSIONS",
            message=f"Insufficient permissions. Required role: {required_role}",
            context={"required_role": required_role},
        )
        self.required_role = required_role
