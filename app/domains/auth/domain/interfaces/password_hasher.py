"""Password hasher interface.

This module defines the interface contract for password hashing operations.
"""

from typing import Protocol

from app.domains.auth.domain.entities import PasswordHash


class PasswordHasher(Protocol):
    """Interface defining the contract for password hasher.

    This interface defines the operations for hashing and verifying passwords.
    """

    def hash_password(self, password: str) -> PasswordHash:
        """Hash a plain text password using bcrypt.

        Args:
            password: Plain text password to hash

        Returns:
            PasswordHash value object containing the bcrypt hash
        """
        ...

    def verify_password(self, plain_password: str, hashed: PasswordHash) -> bool:
        """Verify a plain text password against a hash.

        Args:
            plain_password: Plain text password to verify
            hashed: PasswordHash to compare against

        Returns:
            True if password matches, False otherwise
        """
        ...
