"""Common SQL repository implementation for RestaurantOwner.

This module provides the base SQL implementation that can be shared across
different SQL databases (MySQL, SQLite, PostgreSQL). Database-specific
implementations inherit from this class and only override methods when
database-specific behavior is required.
"""

from datetime import UTC, datetime

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.domain.entities import (
    RestaurantOwner,
    RestaurantOwnerData,
)
from app.domains.restaurants.infrastructure.persistence.models.restaurant_owner import (
    RestaurantOwnerModel,
)
from app.shared.domain.constants import AUDIT_FIELDS_EXCLUDE


class SQLRestaurantOwnerRepository:
    """Common SQL implementation for RestaurantOwner repository.

    This repository provides async CRUD operations for RestaurantOwner entities using
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
        ownership_data: RestaurantOwnerData,
        assigned_by: str | None = None,
        commit: bool = True,
    ) -> RestaurantOwner:
        """Create a new restaurant ownership relationship.

        Args:
            ownership_data: Core ownership data
            assigned_by: ULID of the admin who assigned this ownership
            commit: Whether to commit the transaction immediately

        Returns:
            RestaurantOwner: Complete ownership entity with ID and metadata
        """
        # Create entity - exclude audit fields to prevent conflicts
        entity = RestaurantOwner(
            **ownership_data.model_dump(exclude=AUDIT_FIELDS_EXCLUDE),
            created_by=assigned_by,
            updated_by=assigned_by,
        )

        # Convert to model
        model = RestaurantOwnerModel.model_validate(entity)
        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)
        else:
            await self.session.flush()  # Get ID without committing

        return self._model_to_entity(model)

    async def get_by_id(self, ownership_id: str) -> RestaurantOwner | None:
        """Get an ownership by its ID.

        Args:
            ownership_id: ULID of the ownership

        Returns:
            RestaurantOwner if found, None otherwise
        """
        model = await self.session.get(RestaurantOwnerModel, ownership_id)
        return self._model_to_entity(model) if model else None

    async def get_by_ids(
        self,
        restaurant_id: str,
        owner_id: str,
    ) -> RestaurantOwner | None:
        """Get ownership by restaurant and owner IDs.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner

        Returns:
            RestaurantOwner if found, None otherwise
        """
        statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id,
            RestaurantOwnerModel.owner_id == owner_id,
        )
        result = await self.session.exec(statement)
        model = result.first()
        return self._model_to_entity(model) if model else None

    async def list_by_restaurant(
        self,
        restaurant_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[RestaurantOwner]:
        """List all owners of a restaurant.

        Args:
            restaurant_id: ULID of the restaurant
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of restaurant owners
        """
        statement = (
            select(RestaurantOwnerModel)
            .where(RestaurantOwnerModel.restaurant_id == restaurant_id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.exec(statement)
        models = result.all()
        return [self._model_to_entity(model) for model in models]

    async def list_by_owner(
        self,
        owner_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[RestaurantOwner]:
        """List all restaurants owned by a user.

        Args:
            owner_id: ULID of the owner
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of restaurant ownerships for the user
        """
        statement = (
            select(RestaurantOwnerModel)
            .where(RestaurantOwnerModel.owner_id == owner_id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.exec(statement)
        models = result.all()
        return [self._model_to_entity(model) for model in models]

    async def get_primary_owner(
        self,
        restaurant_id: str,
    ) -> RestaurantOwner | None:
        """Get the primary owner of a restaurant.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            Primary RestaurantOwner if found, None otherwise
        """
        statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id,
            RestaurantOwnerModel.is_primary == True,  # noqa: E712
        )
        result = await self.session.exec(statement)
        model = result.first()
        return self._model_to_entity(model) if model else None

    async def is_owner_of_restaurant(
        self,
        owner_id: str,
        restaurant_id: str,
    ) -> bool:
        """Check if a user is an owner of a specific restaurant.

        Args:
            owner_id: ULID of the user
            restaurant_id: ULID of the restaurant

        Returns:
            True if user is an owner, False otherwise
        """
        model = await self.get_by_ids(restaurant_id, owner_id)
        return model is not None

    async def get_restaurants_by_owner(
        self,
        owner_id: str,
    ) -> list[RestaurantOwner]:
        """Get all restaurants owned by a specific user.

        Args:
            owner_id: ULID of the owner

        Returns:
            List of restaurant ownerships for the user
        """
        statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.owner_id == owner_id
        )
        result = await self.session.exec(statement)
        models = result.all()
        return [self._model_to_entity(model) for model in models]

    async def get_owners_by_restaurant(
        self,
        restaurant_id: str,
    ) -> list[RestaurantOwner]:
        """Get all owners of a specific restaurant.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            List of owners for the restaurant
        """
        statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id
        )
        result = await self.session.exec(statement)
        models = result.all()
        return [self._model_to_entity(model) for model in models]

    async def update(
        self,
        ownership_id: str,
        ownership_data: RestaurantOwnerData,
        updated_by: str | None = None,
        commit: bool = True,
    ) -> RestaurantOwner | None:
        """Update an existing ownership relationship.

        Args:
            ownership_id: ULID of the ownership to update
            ownership_data: Updated ownership data
            updated_by: ULID of the user who updated the record
            commit: Whether to commit the transaction immediately

        Returns:
            Updated RestaurantOwner if found, None otherwise
        """
        model = await self.session.get(RestaurantOwnerModel, ownership_id)
        if not model:
            return None

        # Update fields
        update_data = ownership_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(model, key, value)

        # Update audit fields
        model.updated_at = datetime.now(UTC)
        model.updated_by = updated_by

        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)
        else:
            await self.session.flush()

        return self._model_to_entity(model)

    async def unset_primary_owner(
        self,
        restaurant_id: str,
        commit: bool = True,
    ) -> bool:
        """Unset the primary owner for a restaurant.

        Args:
            restaurant_id: ULID of the restaurant
            commit: Whether to commit the transaction immediately

        Returns:
            True if a primary owner was unset, False if none existed
        """
        statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id,
            RestaurantOwnerModel.is_primary == True,  # noqa: E712
        )
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return False

        model.is_primary = False
        model.updated_at = datetime.now(UTC)
        self.session.add(model)

        if commit:
            await self.session.commit()
        else:
            await self.session.flush()

        return True

    async def delete(
        self,
        ownership_id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Delete an ownership relationship (hard delete).

        Args:
            ownership_id: ULID of the ownership to delete
            deleted_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        model = await self.session.get(RestaurantOwnerModel, ownership_id)
        if not model:
            return False

        await self.session.delete(model)

        if commit:
            await self.session.commit()

        return True

    async def count_by_restaurant(self, restaurant_id: str) -> int:
        """Count owners for a restaurant.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            Number of owners for the restaurant
        """
        statement = select(func.count(RestaurantOwnerModel.id)).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id
        )
        result = await self.session.exec(statement)
        return result.one()

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

    def _model_to_entity(self, model: RestaurantOwnerModel) -> RestaurantOwner:
        """Convert a model to an entity.

        Args:
            model: RestaurantOwnerModel from database

        Returns:
            RestaurantOwner entity
        """
        return RestaurantOwner.model_validate(model)
