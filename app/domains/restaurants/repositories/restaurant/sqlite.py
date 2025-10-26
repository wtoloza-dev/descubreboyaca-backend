"""Restaurant SQLite implementation.

This module provides an asynchronous implementation of the Restaurant
repository for data persistence using SQLModel.
"""

from datetime import UTC, datetime
from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.domain import Restaurant, RestaurantData
from app.domains.restaurants.models.restaurant import RestaurantModel


class RestaurantRepositorySQLite:
    """Restaurant SQLite implementation using async operations.

    Handles persistence of restaurant records using SQLModel with
    asynchronous database operations for optimal performance in FastAPI.

    Attributes:
        session: SQLModel async session for database operations
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the restaurant repository.

        Args:
            session: SQLModel async session for database operations
        """
        self.session = session

    async def create(
        self,
        restaurant_data: RestaurantData,
        created_by: str | None = None,
        commit: bool = True,
    ) -> Restaurant:
        """Create a new restaurant.

        Args:
            restaurant_data: Core restaurant data without system metadata
            created_by: ULID of the user who created the record
            commit: Whether to commit the transaction immediately

        Returns:
            Restaurant: Complete restaurant entity with ID and system metadata
        """
        # Create entity - it generates its own ID and timestamps
        restaurant = Restaurant(
            **restaurant_data.model_dump(),
            created_by=created_by,
            updated_by=created_by,
        )

        # Convert to model - use mode="json" to serialize HttpUrl → str automatically
        model = RestaurantModel.model_validate(restaurant.model_dump(mode="json"))
        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)

        return self._model_to_entity(model)

    async def get_by_id(self, restaurant_id: str) -> Restaurant | None:
        """Get a restaurant by its ID.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            Restaurant if found, None otherwise
        """
        model = await self.session.get(RestaurantModel, restaurant_id)
        if not model:
            return None
        return self._model_to_entity(model)

    async def find(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Restaurant]:
        """Find restaurants with dynamic filters and pagination.

        This method allows querying restaurants with any combination of filters
        by dynamically building the WHERE clause using model attributes.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match RestaurantModel attribute names.
                    Example: {"city": "Tunja", "cuisine_type": "Colombian"}
            offset: Number of records to offset (skip)
            limit: Maximum number of records to return

        Returns:
            List of restaurants matching the filters

        Raises:
            AttributeError: If a filter key doesn't match any model attribute

        Example:
            >>> restaurants = await repo.find()  # Get all
            >>> restaurants = await repo.find({"city": "Tunja"})
            >>> restaurants = await repo.find(
            ...     {"city": "Tunja", "price_level": "medium"}, offset=0, limit=10
            ... )
        """
        statement = select(RestaurantModel)

        # Apply dynamic filters if provided
        if filters:
            for field_name, value in filters.items():
                # Get the model attribute dynamically
                if not hasattr(RestaurantModel, field_name):
                    raise AttributeError(
                        f"RestaurantModel has no attribute '{field_name}'"
                    )

                model_field = getattr(RestaurantModel, field_name)
                statement = statement.where(model_field == value)

        # Apply pagination
        statement = statement.offset(offset).limit(limit)

        result = await self.session.exec(statement)
        models = result.all()

        return [self._model_to_entity(model) for model in models]

    async def update(
        self,
        restaurant_id: str,
        restaurant_data: RestaurantData,
        updated_by: str | None = None,
        commit: bool = True,
    ) -> Restaurant | None:
        """Update an existing restaurant.

        Args:
            restaurant_id: ULID of the restaurant to update
            restaurant_data: Updated restaurant data
            updated_by: ULID of the user who updated the record
            commit: Whether to commit the transaction immediately

        Returns:
            Updated Restaurant if found, None otherwise
        """
        model = await self.session.get(RestaurantModel, restaurant_id)
        if not model:
            return None

        # Update model fields - Pydantic handles value object serialization
        update_data = restaurant_data.model_dump(mode="json")
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

    async def delete(self, restaurant_id: str, commit: bool = True) -> bool:
        """Delete a restaurant (hard delete).

        Args:
            restaurant_id: ULID of the restaurant to delete
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        model = await self.session.get(RestaurantModel, restaurant_id)
        if not model:
            return False

        await self.session.delete(model)

        if commit:
            await self.session.commit()

        return True

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count restaurants with dynamic filters.

        This method allows counting restaurants with any combination of filters
        by dynamically building the WHERE clause using model attributes.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match RestaurantModel attribute names.
                    Example: {"city": "Tunja", "cuisine_type": "Colombian"}

        Returns:
            Count of restaurants matching the filters

        Raises:
            AttributeError: If a filter key doesn't match any model attribute

        Example:
            >>> count = await repo.count({"city": "Tunja"})
            >>> count = await repo.count({"city": "Tunja", "price_level": "medium"})
            >>> count = await repo.count()  # Count all
        """
        from sqlmodel import func

        statement = select(func.count(RestaurantModel.id))

        # Apply dynamic filters if provided
        if filters:
            for field_name, value in filters.items():
                # Get the model attribute dynamically
                if not hasattr(RestaurantModel, field_name):
                    raise AttributeError(
                        f"RestaurantModel has no attribute '{field_name}'"
                    )

                model_field = getattr(RestaurantModel, field_name)
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

    def _model_to_entity(self, model: RestaurantModel) -> Restaurant:
        """Convert a model to an entity.

        Pydantic automatically converts dicts to value objects when validating:
        - dict[str, float] → GeoLocation
        - dict[str, str] → SocialMedia

        Args:
            model: RestaurantModel from database

        Returns:
            Restaurant entity
        """
        return Restaurant.model_validate(model)
