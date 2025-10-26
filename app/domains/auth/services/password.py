"""Bcrypt password hasher implementation.

This module provides password hashing and verification using bcrypt.
"""

import bcrypt

from app.domains.auth.domain.entities import PasswordHash


class BcryptPasswordHasher:
    """Bcrypt-based password hasher implementation.

    This hasher uses bcrypt for secure password hashing.
    Bcrypt is a slow hashing algorithm that is resistant to brute-force attacks.

    Attributes:
        rounds: Number of bcrypt rounds (higher = more secure but slower)
    """

    def __init__(self, rounds: int = 12) -> None:
        """Initialize bcrypt password hasher.

        Args:
            rounds: Number of bcrypt rounds (default: 12)
        """
        self.rounds = rounds

    def hash_password(self, password: str) -> PasswordHash:
        """Hash a plain text password using bcrypt.

        Args:
            password: Plain text password to hash

        Returns:
            PasswordHash value object containing the bcrypt hash
        """
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

        return PasswordHash(value=hashed.decode("utf-8"))

    def verify_password(self, plain_password: str, hashed: PasswordHash) -> bool:
        """Verify a plain text password against a hash.

        Args:
            plain_password: Plain text password to verify
            hashed: PasswordHash to compare against

        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed.value.encode("utf-8")
        )
