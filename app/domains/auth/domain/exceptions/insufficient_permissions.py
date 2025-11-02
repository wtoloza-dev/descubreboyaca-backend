"""Insufficient permissions domain exception."""

from typing import Any

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class InsufficientPermissionsException(AuthenticationException):
    """Exception raised when user lacks required permissions.

    Raised when a user tries to access a resource or perform an operation
    they don't have sufficient permissions for.

    Example:
        >>> raise InsufficientPermissionsException(
        ...     required_role="ADMIN",
        ...     user_role="USER",
        ... )
    """

    def __init__(
        self,
        required_role: str,
        user_role: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize insufficient permissions exception.

        Args:
            required_role: Role required for the operation
            user_role: Optional current user role
            context: Additional context
        """
        full_context = {
            "required_role": required_role,
            **({"user_role": user_role} if user_role else {}),
            **(context or {}),
        }
        super().__init__(
            message=f"Insufficient permissions. Required role: {required_role}",
            context=full_context,
            error_code="INSUFFICIENT_PERMISSIONS",
        )
