"""User repository PostgreSQL implementation.

This module provides the PostgreSQL repository implementation for User persistence operations.
"""

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.domains.auth.domain import User, UserData
from app.domains.auth.models import UserModel


class UserRepositoryPostgreSQL:
    """Repository for User entity persistence using PostgreSQL.

    This repository handles all database operations for users with PostgreSQL,
    implementing the UserRepositoryInterface contract.

    Attributes:
        session: SQLAlchemy async session for database operations
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize user repository.

        Args:
            session: SQLAlchemy async session
        """
        self.session = session

    async def create(self, user_data: UserData, commit: bool = True) -> User:
        """Create a new user.

        The User entity generates its own ID using ULID.

        Args:
            user_data: User data without system metadata
            commit: Whether to commit the transaction immediately

        Returns:
            User: Created user with ID and metadata
        """
        # Create User entity (generates ULID automatically)
        user = User(**user_data.model_dump())

        # Convert to ORM model
        model = UserModel.model_validate(user)

        # Persist
        self.session.add(model)
        if commit:
            await self.session.commit()
            await self.session.refresh(model)

        # Convert back to entity
        return User.model_validate(model)

    async def get_by_id(self, user_id: str) -> User | None:
        """Get a user by their ID.

        Args:
            user_id: ULID of the user

        Returns:
            User if found, None otherwise
        """
        statement = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.exec(statement)
        model = result.one_or_none()

        if model is None:
            return None

        return User.model_validate(model)

    async def get_by_email(self, email: str) -> User | None:
        """Get a user by their email address.

        Args:
            email: Email address of the user

        Returns:
            User if found, None otherwise
        """
        statement = select(UserModel).where(UserModel.email == email)
        result = await self.session.exec(statement)
        model = result.one_or_none()

        if model is None:
            return None

        return User.model_validate(model)

    async def get_by_google_id(self, google_id: str) -> User | None:
        """Get a user by their Google ID.

        Args:
            google_id: Google OAuth unique identifier

        Returns:
            User if found, None otherwise
        """
        statement = select(UserModel).where(UserModel.google_id == google_id)
        result = await self.session.exec(statement)
        model = result.one_or_none()

        if model is None:
            return None

        return User.model_validate(model)

    async def update(
        self, user_id: str, user_data: UserData, commit: bool = True
    ) -> User | None:
        """Update an existing user.

        Args:
            user_id: ULID of the user to update
            user_data: Updated user data
            commit: Whether to commit the transaction immediately

        Returns:
            Updated User if found, None otherwise
        """
        statement = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.exec(statement)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        # Update model fields
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(model, key, value)

        # Update timestamp
        model.updated_at = datetime.now(UTC)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)

        return User.model_validate(model)

    async def deactivate(self, user_id: str, commit: bool = True) -> bool:
        """Deactivate a user (soft delete).

        Args:
            user_id: ULID of the user to deactivate
            commit: Whether to commit the transaction immediately

        Returns:
            True if deactivated, False if not found
        """
        statement = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.exec(statement)
        model = result.scalar_one_or_none()

        if model is None:
            return False

        model.is_active = False
        model.updated_at = datetime.now(UTC)

        if commit:
            await self.session.commit()

        return True

    async def delete(self, user_id: str, commit: bool = True) -> bool:
        """Delete a user (hard delete).

        Args:
            user_id: ULID of the user to delete
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        statement = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.exec(statement)
        model = result.scalar_one_or_none()

        if model is None:
            return False

        await self.session.delete(model)

        if commit:
            await self.session.commit()

        return True

    async def commit(self) -> None:
        """Commit the current transaction."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self.session.rollback()
