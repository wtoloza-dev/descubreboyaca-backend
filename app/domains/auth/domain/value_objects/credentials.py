"""Credentials value object.

This module defines the Credentials value object for authentication.
"""

from pydantic import BaseModel, ConfigDict, Field


class Credentials(BaseModel):
    """Immutable credentials for email/password authentication.

    This represents user credentials for authentication.
    Being frozen (immutable) ensures credentials cannot be modified.

    Attributes:
        email: User's email address
        password: User's plain text password (before hashing)
    """

    model_config = ConfigDict(frozen=True)

    email: str = Field(description="User's email address")
    password: str = Field(description="User's plain text password")

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
