"""Credentials value object.

This module defines the Credentials value object for authentication.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Credentials:
    """Immutable credentials for email/password authentication.

    This represents user credentials for authentication.
    Being frozen (immutable) ensures credentials cannot be modified.

    Attributes:
        email: User's email address
        password: User's plain text password (before hashing)
    """

    email: str
    password: str

    def __str__(self) -> str:
        """Return string representation (masked for security).

        Returns:
            Masked credentials for logging/debugging
        """
        return f"Credentials(email={self.email}, password=***)"

    def __repr__(self) -> str:
        """Return representation (masked for security).

        Returns:
            Masked credentials for logging/debugging
        """
        return f"Credentials(email={self.email}, password=***)"
