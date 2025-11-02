"""Favorite repository implementation.

This module implements the favorite repository for database operations.
"""

from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.favorites.domain.entities import Favorite, FavoriteData
from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.domain.exceptions import FavoriteAlreadyExistsException
from app.domains.favorites.models import FavoriteModel


class FavoriteRepository:
    """Repository for favorite database operations.

    This repository implements the FavoriteRepositoryInterface and provides
    concrete database operations using SQLModel/SQLAlchemy.

    Attributes:
        session: Async SQLModel database session
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            session: Async SQLModel database session
        """
        self.session = session

    async def create(self, favorite_data: FavoriteData) -> Favorite:
        """Create a new favorite.

        The Favorite entity generates its own ID and timestamp following DDD
        principles. The repository only persists the entity to the database.

        Args:
            favorite_data: Data for the new favorite (without ID and timestamp)

        Returns:
            The created favorite entity with generated ID and timestamp

        Raises:
            FavoriteAlreadyExistsException: If the user has already favorited this entity
        """
        # Create entity with auto-generated ID and timestamp
        favorite = Favorite(**favorite_data.model_dump())

        # Convert to ORM model
        model = FavoriteModel.model_validate(favorite)

        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
        except IntegrityError as e:
            await self.session.rollback()
            raise FavoriteAlreadyExistsException(
                user_id=favorite_data.user_id,
                entity_type=favorite_data.entity_type.value,
                entity_id=favorite_data.entity_id,
            ) from e

        return favorite

    async def delete(
        self, user_id: str, entity_type: EntityType, entity_id: str
    ) -> bool:
        """Delete a favorite.

        This is a hard delete - the record is permanently removed from the database.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity

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
        self, user_id: str, entity_type: EntityType, entity_id: str
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
        self, user_id: str, entity_type: EntityType, entity_id: str
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
