"""User repository interface.

This module defines the interface contract for User repository operations.
"""

from typing import Protocol

from app.domains.auth.domain.entities import User, UserData


class UserRepositoryInterface(Protocol):
    """Interface defining the contract for User repository.

    This interface defines the operations that can be performed on
    user data storage using asynchronous operations.
    """

    async def create(self, user_data: UserData, commit: bool = True) -> User:
        """Create a new user asynchronously.

        Args:
            user_data: Core user data without system metadata
            commit: Whether to commit the transaction immediately

        Returns:
            User: Complete user entity with ID and system metadata
        """
        ...

    async def get_by_id(self, user_id: str) -> User | None:
        """Get a user by their ID asynchronously.

        Args:
            user_id: ULID of the user

        Returns:
            User if found, None otherwise
        """
        ...

    async def get_by_email(self, email: str) -> User | None:
        """Get a user by their email address asynchronously.

        Args:
            email: Email address of the user

        Returns:
            User if found, None otherwise
        """
        ...

    async def get_by_google_id(self, google_id: str) -> User | None:
        """Get a user by their Google ID asynchronously.

        Args:
            google_id: Google OAuth unique identifier

        Returns:
            User if found, None otherwise
        """
        ...

    async def update(
        self, user_id: str, user_data: UserData, commit: bool = True
    ) -> User | None:
        """Update an existing user asynchronously.

        Args:
            user_id: ULID of the user to update
            user_data: Updated user data
            commit: Whether to commit the transaction immediately

        Returns:
            Updated User if found, None otherwise
        """
        ...

    async def deactivate(self, user_id: str, commit: bool = True) -> bool:
        """Deactivate a user asynchronously (soft delete).

        Args:
            user_id: ULID of the user to deactivate
            commit: Whether to commit the transaction immediately

        Returns:
            True if deactivated, False if not found
        """
        ...

    async def delete(self, user_id: str, commit: bool = True) -> bool:
        """Delete a user asynchronously (hard delete).

        Args:
            user_id: ULID of the user to delete
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        ...

    async def commit(self) -> None:
        """Commit the current transaction.

        Useful for Unit of Work pattern when commit=False is used in operations.
        """
        ...

    async def rollback(self) -> None:
        """Rollback the current transaction.

        Useful for Unit of Work pattern when an error occurs.
        """
        ...
