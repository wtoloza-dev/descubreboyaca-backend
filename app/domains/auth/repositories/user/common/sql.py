"""Common SQL repository implementation for User.

This module provides the base SQL implementation that can be shared across
different SQL databases (MySQL, SQLite, PostgreSQL). Database-specific
implementations inherit from this class and only override methods when
database-specific behavior is required.
"""

from datetime import UTC, datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.auth.domain import User, UserData
from app.domains.auth.models import UserModel
from app.shared.domain.constants import AUDIT_FIELDS_EXCLUDE


class SQLUserRepository:
    """Common SQL implementation for User repository.

    This repository provides async CRUD operations for User entities using
    SQLAlchemy/SQLModel with async/await support. It handles the conversion
    between infrastructure models (ORM) and domain entities following DDD principles.

    Database-specific implementations (MySQL, SQLite, PostgreSQL) inherit from this
    class and can override methods if needed for specific database behavior.

    Responsibilities:
    - Execute async database queries using SQLModel
    - Convert ORM models to domain entities
    - Handle database-specific logic (transactions, error handling)
    - Return None when entities are not found (not exceptions)

    Note: This repository returns None when entities are not found.
    Business exceptions (NotFound, etc.) should be handled in the Service layer.

    Attributes:
        session: Async SQLAlchemy session for database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the SQL repository with an async database session.

        Args:
            session: Async SQLAlchemy session for database operations.
        """
        self.session = session

    async def create(
        self,
        user_data: UserData,
        created_by: str,
        commit: bool = True,
    ) -> User:
        """Create a new user.

        The User entity generates its own ID using ULID.

        Args:
            user_data: User data without system metadata
            created_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            User: Created user with ID and metadata
        """
        # Create User entity (generates ULID automatically)
        # Exclude audit fields to prevent conflicts
        user = User(
            **user_data.model_dump(exclude=AUDIT_FIELDS_EXCLUDE),
            created_by=created_by,
            updated_by=created_by,
        )

        # Convert to ORM model
        model = UserModel.model_validate(user)

        # Persist
        self.session.add(model)
        if commit:
            await self.session.commit()
            await self.session.refresh(model)
        else:
            await self.session.flush()  # Get ID without committing

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
        model = result.first()

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
        model = result.first()

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
        model = result.first()

        if model is None:
            return None

        return User.model_validate(model)

    async def update(
        self,
        user_id: str,
        user_data: UserData,
        updated_by: str,
        commit: bool = True,
    ) -> User | None:
        """Update an existing user.

        Args:
            user_id: ULID of the user to update
            user_data: Updated user data
            updated_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            Updated User if found, None otherwise
        """
        statement = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.exec(statement)
        model = result.first()

        if model is None:
            return None

        # Update model fields
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(model, key, value)

        # Update audit fields
        model.updated_at = datetime.now(UTC)
        model.updated_by = updated_by

        if commit:
            await self.session.commit()
            await self.session.refresh(model)
        else:
            await self.session.flush()

        return User.model_validate(model)

    async def deactivate(
        self,
        user_id: str,
        updated_by: str,
        commit: bool = True,
    ) -> bool:
        """Deactivate a user (soft delete).

        Args:
            user_id: ULID of the user to deactivate
            updated_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            True if deactivated, False if not found
        """
        statement = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.exec(statement)
        model = result.first()

        if model is None:
            return False

        model.is_active = False
        model.updated_at = datetime.now(UTC)
        model.updated_by = updated_by

        if commit:
            await self.session.commit()
        else:
            await self.session.flush()

        return True

    async def delete(
        self,
        user_id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Delete a user (hard delete).

        Args:
            user_id: ULID of the user to delete
            deleted_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        statement = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.exec(statement)
        model = result.first()

        if model is None:
            return False

        await self.session.delete(model)

        if commit:
            await self.session.commit()

        return True

    async def commit(self) -> None:
        """Commit the current transaction.

        Commits all pending changes in the current database session.
        """
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction.

        Rolls back all pending changes in the current database session.
        """
        await self.session.rollback()
