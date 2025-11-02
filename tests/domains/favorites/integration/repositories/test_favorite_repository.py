"""Integration tests for FavoriteRepository (SQLite).

One operation per file/group kept small, per testing architecture.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from ulid import ULID

from app.domains.favorites.domain.entities import FavoriteData
from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.domain.exceptions import FavoriteAlreadyExistsException
from app.domains.favorites.repositories import FavoriteRepository


class TestFavoriteRepositoryCreate:
    """Tests for create operation."""

    @pytest.mark.asyncio
    async def test_create_persists_and_returns_entity(self, test_session: AsyncSession):
        repo = FavoriteRepository(test_session)
        data = FavoriteData(
            user_id=str(ULID()),
            entity_type=EntityType.RESTAURANT,
            entity_id=str(ULID()),
        )
        created = await repo.create(data)

        assert created.user_id == data.user_id
        assert created.entity_type == data.entity_type
        assert created.entity_id == data.entity_id

    @pytest.mark.asyncio
    async def test_create_duplicate_raises(self, test_session: AsyncSession):
        repo = FavoriteRepository(test_session)
        data = FavoriteData(
            user_id=str(ULID()),
            entity_type=EntityType.DISH,
            entity_id=str(ULID()),
        )
        await repo.create(data)

        with pytest.raises(FavoriteAlreadyExistsException):
            await repo.create(data)


class TestFavoriteRepositoryDeleteAndExists:
    """Tests for delete and exists operations."""

    @pytest.mark.asyncio
    async def test_exists_and_delete_flow(self, test_session: AsyncSession):
        repo = FavoriteRepository(test_session)
        data = FavoriteData(
            user_id=str(ULID()),
            entity_type=EntityType.RESTAURANT,
            entity_id=str(ULID()),
        )
        await repo.create(data)

        assert await repo.exists(data.user_id, data.entity_type, data.entity_id)

        deleted = await repo.delete(data.user_id, data.entity_type, data.entity_id)
        assert deleted is True

        assert not await repo.exists(data.user_id, data.entity_type, data.entity_id)


class TestFavoriteRepositoryGetAndList:
    """Tests for get and get_by_user operations."""

    @pytest.mark.asyncio
    async def test_get_and_list_by_user(self, test_session: AsyncSession):
        repo = FavoriteRepository(test_session)
        user_id = str(ULID())

        # Seed two favorites for same user
        await repo.create(
            FavoriteData(
                user_id=user_id,
                entity_type=EntityType.RESTAURANT,
                entity_id=str(ULID()),
            )
        )
        second_entity_id = str(ULID())
        await repo.create(
            FavoriteData(
                user_id=user_id,
                entity_type=EntityType.DISH,
                entity_id=second_entity_id,
            )
        )

        # get()
        fav = await repo.get(
            user_id=user_id,
            entity_type=EntityType.DISH,
            entity_id=second_entity_id,
        )
        assert fav is not None
        assert fav.entity_type is EntityType.DISH

        # get_by_user() without filter
        items, total = await repo.get_by_user(user_id=user_id, offset=0, limit=10)
        assert total == 2
        assert len(items) == 2

        # get_by_user() with type filter
        items2, total2 = await repo.get_by_user(
            user_id=user_id, entity_type=EntityType.RESTAURANT, offset=0, limit=10
        )
        assert total2 == 1
        assert len(items2) == 1
