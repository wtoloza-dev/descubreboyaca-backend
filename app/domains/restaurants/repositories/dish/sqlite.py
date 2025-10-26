"""Dish SQLite implementation.

This module provides an asynchronous implementation of the Dish
repository for data persistence using SQLModel.
"""

from datetime import UTC, datetime
from typing import Any

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.domain import Dish, DishData
from app.domains.restaurants.models.dish import DishModel


class DishRepositorySQLite:
    """Dish SQLite implementation using async operations.

    Handles persistence of dish records using SQLModel with
    asynchronous database operations for optimal performance in FastAPI.

    Attributes:
        session: SQLModel async session for database operations
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the dish repository.

        Args:
            session: SQLModel async session for database operations
        """
        self.session = session

    async def create(
        self,
        dish_data: DishData,
        restaurant_id: str,
        created_by: str | None = None,
        commit: bool = True,
    ) -> Dish:
        """Create a new dish.

        Args:
            dish_data: Core dish data without system metadata
            restaurant_id: ULID of the restaurant this dish belongs to
            created_by: ULID of the user who created the record
            commit: Whether to commit the transaction immediately

        Returns:
            Dish: Complete dish entity with ID and system metadata
        """
        # Create entity - it generates its own ID and timestamps (inherited from Audit)
        dish = Dish(
            **dish_data.model_dump(),
            restaurant_id=restaurant_id,
            created_by=created_by,
            updated_by=created_by,
        )

        # Convert to model - use mode="json" to serialize HttpUrl → str automatically
        model = DishModel.model_validate(dish.model_dump(mode="json"))
        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)

        return self._model_to_entity(model)

    async def get_by_id(self, dish_id: str) -> Dish | None:
        """Get a dish by its ID.

        Args:
            dish_id: ULID of the dish

        Returns:
            Dish if found, None otherwise
        """
        model = await self.session.get(DishModel, dish_id)
        if not model:
            return None
        return self._model_to_entity(model)

    async def get_by_restaurant_id(
        self,
        restaurant_id: str,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Dish]:
        """Get all dishes for a specific restaurant.

        Args:
            restaurant_id: ULID of the restaurant
            filters: Optional additional filters (category, is_available, etc.)
            offset: Number of records to offset (skip)
            limit: Maximum number of records to return

        Returns:
            List of dishes belonging to the restaurant
        """
        statement = select(DishModel).where(DishModel.restaurant_id == restaurant_id)

        # Apply additional filters if provided
        if filters:
            for field_name, value in filters.items():
                if not hasattr(DishModel, field_name):
                    raise AttributeError(f"DishModel has no attribute '{field_name}'")

                model_field = getattr(DishModel, field_name)
                statement = statement.where(model_field == value)

        # Order by display_order, then by name
        statement = statement.order_by(DishModel.display_order, DishModel.name)

        # Apply pagination
        statement = statement.offset(offset).limit(limit)

        result = await self.session.exec(statement)
        models = result.all()

        return [self._model_to_entity(model) for model in models]

    async def find(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Dish]:
        """Find dishes with dynamic filters and pagination.

        This method allows querying dishes with any combination of filters
        by dynamically building the WHERE clause using model attributes.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match DishModel attribute names.
                    Example: {"category": "appetizer", "is_available": True}
            offset: Number of records to offset (skip)
            limit: Maximum number of records to return

        Returns:
            List of dishes matching the filters

        Raises:
            AttributeError: If a filter key doesn't match any model attribute

        Example:
            >>> dishes = await repo.find()  # Get all
            >>> dishes = await repo.find({"category": "dessert"})
            >>> dishes = await repo.find(
            ...     {"is_available": True, "is_featured": True}, offset=0, limit=10
            ... )
        """
        statement = select(DishModel)

        # Apply dynamic filters if provided
        if filters:
            for field_name, value in filters.items():
                # Get the model attribute dynamically
                if not hasattr(DishModel, field_name):
                    raise AttributeError(f"DishModel has no attribute '{field_name}'")

                model_field = getattr(DishModel, field_name)
                statement = statement.where(model_field == value)

        # Order by display_order, then by name
        statement = statement.order_by(DishModel.display_order, DishModel.name)

        # Apply pagination
        statement = statement.offset(offset).limit(limit)

        result = await self.session.exec(statement)
        models = result.all()

        return [self._model_to_entity(model) for model in models]

    async def update(
        self,
        dish_id: str,
        dish_data: DishData,
        updated_by: str | None = None,
        commit: bool = True,
    ) -> Dish | None:
        """Update an existing dish.

        Args:
            dish_id: ULID of the dish to update
            dish_data: Updated dish data
            updated_by: ULID of the user who updated the record
            commit: Whether to commit the transaction immediately

        Returns:
            Updated Dish if found, None otherwise
        """
        model = await self.session.get(DishModel, dish_id)
        if not model:
            return None

        # Update model fields - Pydantic handles serialization
        update_data = dish_data.model_dump(mode="json")
        for key, value in update_data.items():
            setattr(model, key, value)

        # Update metadata
        model.updated_at = datetime.now(UTC)
        model.updated_by = updated_by

        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)

        return self._model_to_entity(model)

    async def delete(self, dish_id: str, commit: bool = True) -> bool:
        """Delete a dish (hard delete).

        Args:
            dish_id: ULID of the dish to delete
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        model = await self.session.get(DishModel, dish_id)
        if not model:
            return False

        await self.session.delete(model)

        if commit:
            await self.session.commit()

        return True

    async def count(
        self,
        filters: dict[str, Any] | None = None,
    ) -> int:
        """Count dishes with dynamic filters.

        This method allows counting dishes with any combination of filters
        by dynamically building the WHERE clause using model attributes.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match DishModel attribute names.

        Returns:
            Count of dishes matching the filters

        Raises:
            AttributeError: If a filter key doesn't match any model attribute

        Example:
            >>> count = await repo.count()  # Count all
            >>> count = await repo.count({"is_available": True})
        """
        statement = select(func.count(DishModel.id))

        # Apply dynamic filters if provided
        if filters:
            for field_name, value in filters.items():
                # Get the model attribute dynamically
                if not hasattr(DishModel, field_name):
                    raise AttributeError(f"DishModel has no attribute '{field_name}'")

                model_field = getattr(DishModel, field_name)
                statement = statement.where(model_field == value)

        result = await self.session.exec(statement)
        return result.one()

    async def count_by_restaurant_id(
        self,
        restaurant_id: str,
        filters: dict[str, Any] | None = None,
    ) -> int:
        """Count dishes for a specific restaurant.

        Args:
            restaurant_id: ULID of the restaurant
            filters: Optional additional filters (category, is_available, etc.)

        Returns:
            Count of dishes belonging to the restaurant

        Raises:
            AttributeError: If a filter key doesn't match any model attribute
        """
        statement = select(func.count(DishModel.id)).where(
            DishModel.restaurant_id == restaurant_id
        )

        # Apply additional filters if provided
        if filters:
            for field_name, value in filters.items():
                if not hasattr(DishModel, field_name):
                    raise AttributeError(f"DishModel has no attribute '{field_name}'")

                model_field = getattr(DishModel, field_name)
                statement = statement.where(model_field == value)

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

    def _model_to_entity(self, model: DishModel) -> Dish:
        """Convert a model to an entity.

        Pydantic automatically converts data to proper types when validating.

        Args:
            model: DishModel from database

        Returns:
            Dish entity
        """
        return Dish.model_validate(model)
