"""Common SQL repository implementation for Favorite.

This module provides the base SQL implementation that can be shared across
different SQL databases (MySQL, SQLite, PostgreSQL). Database-specific
implementations inherit from this class and only override methods when
database-specific behavior is required.
"""

from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.favorites.domain.entities import Favorite, FavoriteData
from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.domain.exceptions import FavoriteAlreadyExistsException
from app.domains.favorites.infrastructure.persistence.models import FavoriteModel
from app.shared.domain.constants import AUDIT_FIELDS_EXCLUDE


class SQLFavoriteRepository:
    """Common SQL implementation for Favorite repository.

    This repository provides async CRUD operations for Favorite entities using
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
        favorite_data: FavoriteData,
        created_by: str,
        commit: bool = True,
    ) -> Favorite:
        """Create a new favorite.

        Args:
            favorite_data: Data for the new favorite
            created_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            The created favorite entity with generated ID and timestamp

        Raises:
            FavoriteAlreadyExistsException: If the user has already favorited this entity
        """
        # Create Favorite entity (generates ULID automatically)
        # Exclude audit fields to prevent conflicts
        favorite = Favorite(
            **favorite_data.model_dump(exclude=AUDIT_FIELDS_EXCLUDE),
            created_by=created_by,
            updated_by=created_by,
        )

        # Convert to ORM model
        model = FavoriteModel.model_validate(favorite)

        try:
            self.session.add(model)
            if commit:
                await self.session.commit()
                await self.session.refresh(model)
            else:
                await self.session.flush()  # Get ID without committing
        except IntegrityError as e:
            await self.session.rollback()
            raise FavoriteAlreadyExistsException(
                user_id=favorite_data.user_id,
                entity_type=favorite_data.entity_type.value,
                entity_id=favorite_data.entity_id,
            ) from e

        # Convert back to entity
        return Favorite.model_validate(model)

    async def delete(
        self,
        user_id: str,
        entity_type: EntityType,
        entity_id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Delete a favorite (hard delete).

        This is a hard delete - the record is permanently removed from the database.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity
            deleted_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        statement = select(FavoriteModel).where(
            FavoriteModel.user_id == user_id,
            FavoriteModel.entity_type == entity_type,
            FavoriteModel.entity_id == entity_id,
        )
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return False

        await self.session.delete(model)

        if commit:
            await self.session.commit()

        return True

    async def get_by_user(
        self,
        user_id: str,
        entity_type: EntityType | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Favorite], int]:
        """Get favorites for a user with pagination.

        Args:
            user_id: ULID of the user
            entity_type: Optional filter by entity type
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of favorites, total count)
        """
        # Build base query
        statement = select(FavoriteModel).where(FavoriteModel.user_id == user_id)

        # Add entity type filter if provided
        if entity_type:
            statement = statement.where(FavoriteModel.entity_type == entity_type)

        # Count total
        count_statement = select(func.count()).select_from(statement.subquery())
        count_result = await self.session.exec(count_statement)
        total = count_result.one()

        # Apply pagination and ordering
        statement = (
            statement.order_by(FavoriteModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        # Execute query
        result = await self.session.exec(statement)
        models = result.all()

        # Convert to domain entities
        favorites = [Favorite.model_validate(model) for model in models]

        return favorites, total

    async def exists(
        self,
        user_id: str,
        entity_type: EntityType,
        entity_id: str,
    ) -> bool:
        """Check if a favorite exists.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity

        Returns:
            True if favorite exists, False otherwise
        """
        statement = select(func.count()).where(
            FavoriteModel.user_id == user_id,
            FavoriteModel.entity_type == entity_type.value,
            FavoriteModel.entity_id == entity_id,
        )
        result = await self.session.exec(statement)
        count = result.one()
        return count > 0

    async def get(
        self,
        user_id: str,
        entity_type: EntityType,
        entity_id: str,
    ) -> Favorite | None:
        """Get a specific favorite.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity

        Returns:
            The favorite if found, None otherwise
        """
        statement = select(FavoriteModel).where(
            FavoriteModel.user_id == user_id,
            FavoriteModel.entity_type == entity_type,
            FavoriteModel.entity_id == entity_id,
        )
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return None

        return Favorite.model_validate(model)

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
