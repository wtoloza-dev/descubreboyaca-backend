"""Integration tests for FavoriteService.

Focus on service orchestration and error propagation.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from ulid import ULID

from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.domain.exceptions import (
    FavoriteAlreadyExistsException,
    FavoriteNotFoundException,
)
from app.domains.favorites.repositories import SQLiteFavoriteRepository
from app.domains.favorites.services import FavoriteService


@pytest.mark.asyncio
async def test_add_and_check_favorite(test_session: AsyncSession):
    """Test adding a favorite and checking if it exists."""
    repo = SQLiteFavoriteRepository(test_session)
    service = FavoriteService(repo)

    user_id = str(ULID())
    entity_id = str(ULID())

    created = await service.add_favorite(user_id, EntityType.RESTAURANT, entity_id)
    assert created.user_id == user_id

    exists = await service.check_favorite(user_id, EntityType.RESTAURANT, entity_id)
    assert exists is not None


@pytest.mark.asyncio
async def test_add_duplicate_raises(test_session: AsyncSession):
    """Test that adding duplicate favorite raises exception."""
    repo = SQLiteFavoriteRepository(test_session)
    service = FavoriteService(repo)

    user_id = str(ULID())
    entity_id = str(ULID())

    await service.add_favorite(user_id, EntityType.DISH, entity_id)

    with pytest.raises(FavoriteAlreadyExistsException):
        await service.add_favorite(user_id, EntityType.DISH, entity_id)


@pytest.mark.asyncio
async def test_remove_and_list(test_session: AsyncSession):
    """Test removing a favorite and listing remaining favorites."""
    repo = SQLiteFavoriteRepository(test_session)
    service = FavoriteService(repo)

    user_id = str(ULID())
    e1 = str(ULID())
    e2 = str(ULID())

    await service.add_favorite(user_id, EntityType.RESTAURANT, e1)
    await service.add_favorite(user_id, EntityType.DISH, e2)

    items, total = await service.list_favorites(user_id, None, 0, 10)
    assert total == 2
    assert len(items) == 2

    await service.remove_favorite(user_id, EntityType.RESTAURANT, e1)

    items2, total2 = await service.list_favorites(user_id, None, 0, 10)
    assert total2 == 1
    assert len(items2) == 1


@pytest.mark.asyncio
async def test_remove_nonexistent_raises(test_session: AsyncSession):
    """Test that removing nonexistent favorite raises exception."""
    repo = SQLiteFavoriteRepository(test_session)
    service = FavoriteService(repo)

    with pytest.raises(FavoriteNotFoundException):
        await service.remove_favorite(str(ULID()), EntityType.RESTAURANT, str(ULID()))
