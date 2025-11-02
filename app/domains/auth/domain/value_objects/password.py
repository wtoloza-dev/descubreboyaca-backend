"""Password domain value object.

This module defines the PasswordHash value object for handling hashed passwords.
"""

from pydantic import BaseModel, ConfigDict, Field


class PasswordHash(BaseModel):
    """Immutable value object for hashed passwords.

    This represents a bcrypt-hashed password. Being frozen (immutable)
    ensures that password hashes cannot be modified after creation.

    Attributes:
        value: The bcrypt hashed password string
    """

    model_config = ConfigDict(frozen=True)

    value: str = Field(description="Bcrypt hashed password string")

    def __str__(self) -> str:
        """Return string representation (masked for security).

        Returns:
            Masked password hash for logging/debugging
        """
        return "PasswordHash(***)"

    def __repr__(self) -> str:
        """Return representation (masked for security).

        Returns:
            Masked password hash for logging/debugging
        """
        return "PasswordHash(***)"
