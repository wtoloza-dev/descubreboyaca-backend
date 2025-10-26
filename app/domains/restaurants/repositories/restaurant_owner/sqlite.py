"""Restaurant owner repository implementation.

This module provides an asynchronous implementation of the RestaurantOwner
repository for managing restaurant ownership relationships.
"""

from datetime import UTC, datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.domain.entities import (
    RestaurantOwner,
    RestaurantOwnerData,
)
from app.domains.restaurants.models.restaurant_owner import RestaurantOwnerModel


class RestaurantOwnerRepositorySQLite:
    """Restaurant owner SQLite implementation using async operations.

    Handles persistence of restaurant ownership relationships using SQLModel
    with asynchronous database operations for optimal performance.

    Attributes:
        session: SQLModel async session for database operations
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the restaurant owner repository.

        Args:
            session: SQLModel async session for database operations
        """
        self.session = session

    async def assign_owner(
        self,
        owner_data: RestaurantOwnerData,
        assigned_by: str | None = None,
        commit: bool = True,
    ) -> RestaurantOwner:
        """Assign an owner to a restaurant.

        Args:
            owner_data: Restaurant owner data with restaurant_id, owner_id, role, is_primary
            assigned_by: ULID of the admin who assigned this ownership
            commit: Whether to commit the transaction immediately

        Returns:
            RestaurantOwner: The created ownership relationship entity
        """
        # Create entity
        entity = RestaurantOwner(
            **owner_data.model_dump(),
            created_by=assigned_by,
            updated_by=assigned_by,
        )

        # Convert to model
        model = RestaurantOwnerModel.model_validate(entity)
        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)

        return self._model_to_entity(model)

    async def remove_owner(
        self,
        restaurant_id: str,
        owner_id: str,
        commit: bool = True,
    ) -> bool:
        """Remove an owner from a restaurant.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner to remove
            commit: Whether to commit the transaction immediately

        Returns:
            True if removed, False if relationship didn't exist
        """
        statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id,
            RestaurantOwnerModel.owner_id == owner_id,
        )
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return False

        await self.session.delete(model)

        if commit:
            await self.session.commit()

        return True

    async def get_by_ids(
        self,
        restaurant_id: str,
        owner_id: str,
    ) -> RestaurantOwner | None:
        """Get ownership relationship by restaurant and owner IDs.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner

        Returns:
            RestaurantOwner if relationship exists, None otherwise
        """
        statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id,
            RestaurantOwnerModel.owner_id == owner_id,
        )
        result = await self.session.exec(statement)
        model = result.first()
        return self._model_to_entity(model) if model else None

    async def get_restaurants_by_owner(
        self,
        owner_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[RestaurantOwner]:
        """Get all restaurants owned by a specific user.

        Args:
            owner_id: ULID of the owner
            offset: Number of records to offset
            limit: Maximum number of records to return

        Returns:
            List of restaurant ownership relationship entities
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

    async def get_owners_by_restaurant(
        self,
        restaurant_id: str,
    ) -> list[RestaurantOwner]:
        """Get all owners of a specific restaurant.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            List of restaurant ownership relationship entities
        """
        statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id
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
            RestaurantOwner if primary owner exists, None otherwise
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
        """Check if a user is an owner of a restaurant.

        Args:
            owner_id: ULID of the user
            restaurant_id: ULID of the restaurant

        Returns:
            True if user is owner, False otherwise
        """
        model = await self.get_by_ids(restaurant_id, owner_id)
        return model is not None

    async def update_role(
        self,
        restaurant_id: str,
        owner_id: str,
        role: str,
        updated_by: str | None = None,
        commit: bool = True,
    ) -> RestaurantOwner | None:
        """Update the role of an owner.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner
            role: New role (owner, manager, staff)
            updated_by: ULID of the admin who updated the role
            commit: Whether to commit the transaction immediately

        Returns:
            Updated RestaurantOwner if found, None otherwise
        """
        statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id,
            RestaurantOwnerModel.owner_id == owner_id,
        )
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return None

        model.role = role
        model.updated_at = datetime.now(UTC)
        model.updated_by = updated_by

        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)

        return self._model_to_entity(model)

    async def set_primary_owner(
        self,
        restaurant_id: str,
        owner_id: str,
        updated_by: str | None = None,
        commit: bool = True,
    ) -> RestaurantOwner | None:
        """Set a user as the primary owner of a restaurant.

        This method automatically unsets any existing primary owner
        before setting the new one.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner to set as primary
            updated_by: ULID of the admin who made the change
            commit: Whether to commit the transaction immediately

        Returns:
            Updated RestaurantOwner if found, None otherwise
        """
        # First, unset any existing primary owner
        current_primary_statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id,
            RestaurantOwnerModel.is_primary == True,  # noqa: E712
        )
        current_primary_result = await self.session.exec(current_primary_statement)
        current_primary_model = current_primary_result.first()

        if current_primary_model and current_primary_model.owner_id != owner_id:
            current_primary_model.is_primary = False
            current_primary_model.updated_at = datetime.now(UTC)
            current_primary_model.updated_by = updated_by
            self.session.add(current_primary_model)

        # Set the new primary owner
        statement = select(RestaurantOwnerModel).where(
            RestaurantOwnerModel.restaurant_id == restaurant_id,
            RestaurantOwnerModel.owner_id == owner_id,
        )
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return None

        model.is_primary = True
        model.updated_at = datetime.now(UTC)
        model.updated_by = updated_by

        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)

        return self._model_to_entity(model)

    async def count_restaurants_by_owner(self, owner_id: str) -> int:
        """Count total restaurants owned by a user.

        Args:
            owner_id: ULID of the owner

        Returns:
            Count of restaurants
        """
        from sqlmodel import func

        statement = select(func.count(RestaurantOwnerModel.restaurant_id)).where(
            RestaurantOwnerModel.owner_id == owner_id
        )
        result = await self.session.exec(statement)
        return result.one()

    async def commit(self) -> None:
        """Commit the current transaction.

        Useful for Unit of Work pattern when commit=False is used in operations.
        """
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction.

        Useful for Unit of Work pattern when an error occurs.
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
