"""Common SQL repository implementation for Restaurant.

This module provides the base SQL implementation that can be shared across
different SQL databases (MySQL, SQLite, PostgreSQL). Database-specific
implementations inherit from this class and only override methods when
database-specific behavior is required.
"""

from datetime import UTC, datetime
from typing import Any

from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.domain import Restaurant, RestaurantData
from app.domains.restaurants.models.restaurant import RestaurantModel
from app.shared.domain.constants import AUDIT_FIELDS_EXCLUDE


class SQLRestaurantRepository:
    """Common SQL implementation for Restaurant repository.

    This repository provides async CRUD operations for Restaurant entities using
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
        # Exclude audit fields to prevent conflicts
        restaurant = Restaurant(
            **restaurant_data.model_dump(exclude=AUDIT_FIELDS_EXCLUDE),
            created_by=created_by,
            updated_by=created_by,
        )

        # Convert to model - use mode="json" to serialize HttpUrl → str automatically
        model = RestaurantModel.model_validate(restaurant.model_dump(mode="json"))
        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)
        else:
            await self.session.flush()  # Get ID without committing

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
        update_data = restaurant_data.model_dump(mode="json", exclude_unset=True)
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

    async def delete(
        self,
        restaurant_id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Delete a restaurant (hard delete).

        Args:
            restaurant_id: ULID of the restaurant to delete
            deleted_by: User identifier for audit trail
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

    async def deactivate(
        self,
        restaurant_id: str,
        updated_by: str | None = None,
    ) -> bool:
        """Deactivate a restaurant asynchronously.

        Note: This is a placeholder method for future soft-delete functionality.
        Currently, the project uses the archive pattern for deletions.
        If you need to add is_active or is_deleted fields to RestaurantModel,
        uncomment the implementation below.

        Args:
            restaurant_id: ULID of the restaurant to deactivate
            updated_by: ULID of the user who deactivated the record

        Returns:
            True if deactivated, False if not found
        """
        model = await self.session.get(RestaurantModel, restaurant_id)
        if not model:
            return False

        # TODO: Add is_active field to RestaurantModel if soft-delete is needed
        # if hasattr(model, "is_active"):
        #     model.is_active = False

        model.updated_at = datetime.now(UTC)
        model.updated_by = updated_by

        self.session.add(model)
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

        Commits all pending changes in the current database session.
        """
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction.

        Rolls back all pending changes in the current database session.
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
