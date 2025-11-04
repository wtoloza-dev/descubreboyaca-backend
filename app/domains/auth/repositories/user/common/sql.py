"""Common SQL repository implementation for User.

This module provides the base SQL implementation that can be shared across
different SQL databases (MySQL, SQLite, PostgreSQL). Database-specific
implementations inherit from this class and only override methods when
database-specific behavior is required.
"""

from datetime import UTC, datetime
from typing import Any

from sqlmodel import func, select
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
        created_by: str | None = None,
        commit: bool = True,
    ) -> User:
        """Create a new user.

        The User entity generates its own ID using ULID.

        Args:
            user_data: User data without system metadata
            created_by: User identifier for audit trail (None for self-registration)
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

        # For self-registration, use user's own ID as created_by
        if created_by is None:
            user.created_by = user.id
            user.updated_by = user.id

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

    async def find(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[User]:
        """Find users with dynamic filters and pagination.

        This method allows querying users with any combination of filters
        by dynamically building the WHERE clause using model attributes.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match UserModel attribute names.
                    Example: {"role": "admin", "is_active": True}
            offset: Number of records to offset (skip)
            limit: Maximum number of records to return

        Returns:
            List of users matching the filters

        Raises:
            AttributeError: If a filter key doesn't match any model attribute

        Example:
            >>> users = await repo.find()  # Get all
            >>> users = await repo.find({"role": "admin"})
            >>> users = await repo.find(
            ...     {"role": "owner", "is_active": True}, offset=0, limit=10
            ... )
        """
        statement = select(UserModel)

        # Apply dynamic filters if provided
        if filters:
            for field_name, value in filters.items():
                # Get the model attribute dynamically
                if not hasattr(UserModel, field_name):
                    raise AttributeError(f"UserModel has no attribute '{field_name}'")

                model_field = getattr(UserModel, field_name)
                statement = statement.where(model_field == value)

        # Apply pagination
        statement = statement.offset(offset).limit(limit)

        result = await self.session.exec(statement)
        models = result.all()

        return [User.model_validate(model) for model in models]

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count users with dynamic filters.

        This method allows counting users with any combination of filters
        by dynamically building the WHERE clause using model attributes.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match UserModel attribute names.
                    Example: {"role": "admin", "is_active": True}

        Returns:
            Count of users matching the filters

        Raises:
            AttributeError: If a filter key doesn't match any model attribute

        Example:
            >>> total = await repo.count()  # Count all users
            >>> admins = await repo.count({"role": "admin"})
            >>> active_owners = await repo.count({"role": "owner", "is_active": True})
        """
        statement = select(func.count()).select_from(UserModel)

        # Apply dynamic filters if provided
        if filters:
            for field_name, value in filters.items():
                # Get the model attribute dynamically
                if not hasattr(UserModel, field_name):
                    raise AttributeError(f"UserModel has no attribute '{field_name}'")

                model_field = getattr(UserModel, field_name)
                statement = statement.where(model_field == value)

        result = await self.session.exec(statement)
        return result.one()

    async def update(
        self,
        user_id: str,
        user_data: UserData,
        updated_by: str | None = None,
        commit: bool = True,
    ) -> User | None:
        """Update an existing user.

        Args:
            user_id: ULID of the user to update
            user_data: Updated user data
            updated_by: User identifier for audit trail (None for self-update)
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
        # For self-update, use user's own ID as updated_by
        model.updated_by = updated_by if updated_by is not None else user_id

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
