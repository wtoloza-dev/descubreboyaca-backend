"""Integration tests for RestaurantService delete operations.

This module tests the delete_restaurant method with focus on:
- Unit of Work atomicity
- Transaction rollback on failures
- Archive and delete coordination
"""

from unittest.mock import AsyncMock, Mock

import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.audit.infrastructure.persistence.models import ArchiveModel
from app.domains.audit.infrastructure.persistence.repositories import (
    SQLiteArchiveRepository,
)
from app.domains.restaurants.application.services import RestaurantService
from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.domains.restaurants.infrastructure.persistence.models import RestaurantModel
from app.domains.restaurants.infrastructure.persistence.repositories import (
    SQLiteRestaurantRepository,
)


class TestRestaurantServiceDeleteSuccess:
    """Test suite for successful delete operations."""

    @pytest.mark.asyncio
    async def test_delete_with_archive_success(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test successful delete with archive creation.

        Given: A restaurant exists and archive repository is configured
        When: Calling delete_restaurant
        Then: Both restaurant is deleted and archive is created
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        restaurant_id = restaurant.id

        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)

        # Act
        await service.delete_restaurant(
            restaurant_id=restaurant_id,
            deleted_by="user123",
            note="Test deletion",
        )

        # Assert - Restaurant deleted
        result = await test_session.exec(
            select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
        )
        assert result.first() is None

        # Assert - Archive created
        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == restaurant_id)
        )
        archive = result.first()
        assert archive is not None
        assert archive.original_table == "restaurants"
        assert archive.data["name"] == "Test Restaurant"
        assert archive.note == "Test deletion"


class TestRestaurantServiceDeleteAtomicity:
    """Test suite for delete atomicity using Unit of Work pattern.

    These tests verify that the Unit of Work correctly handles failures
    by rolling back all operations when any operation fails.
    """

    @pytest.mark.asyncio
    async def test_delete_rollback_when_archive_fails(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test that restaurant is NOT deleted if archive creation fails.

        Given: A restaurant exists and archive repository will fail
        When: Calling delete_restaurant and archive fails
        Then: Restaurant is NOT deleted (rollback successful)
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Rollback")
        restaurant_id = restaurant.id

        restaurant_repo = SQLiteRestaurantRepository(test_session)

        # Mock archive repository to fail
        mock_archive_repo = Mock()
        mock_archive_repo.create = AsyncMock(
            side_effect=Exception("Simulated archive failure")
        )
        mock_archive_repo.session = test_session  # Needed for UoW

        service = RestaurantService(restaurant_repo, mock_archive_repo)

        # Act & Assert - Should raise exception
        with pytest.raises(Exception, match="Simulated archive failure"):
            await service.delete_restaurant(
                restaurant_id=restaurant_id,
                deleted_by="user123",
                note="Should rollback",
            )

        # Assert - Restaurant still exists (rollback worked)
        result = await test_session.exec(
            select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
        )
        restaurant_after = result.first()
        assert restaurant_after is not None
        assert restaurant_after.name == "Test Rollback"

        # Assert - No archive created
        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == restaurant_id)
        )
        assert result.first() is None

    @pytest.mark.asyncio
    async def test_delete_rollback_when_delete_fails(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test that archive is NOT created if restaurant delete fails.

        Given: A restaurant exists and delete will fail
        When: Calling delete_restaurant and delete fails
        Then: Archive is NOT created (rollback successful)
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Delete Fail")
        restaurant_id = restaurant.id

        archive_repo = SQLiteArchiveRepository(test_session)

        # Mock restaurant repository to fail on delete
        mock_restaurant_repo = Mock()
        mock_restaurant_repo.session = test_session  # Needed for UoW

        # get_by_id succeeds (so we pass validation)
        async def mock_get_by_id(id: str):
            result = await test_session.exec(
                select(RestaurantModel).where(RestaurantModel.id == id)
            )
            model = result.first()
            if not model:
                raise RestaurantNotFoundException(id)
            from app.domains.restaurants.domain import Restaurant

            return Restaurant.model_validate(model)

        mock_restaurant_repo.get_by_id = mock_get_by_id

        # delete fails
        mock_restaurant_repo.delete = AsyncMock(
            side_effect=Exception("Simulated delete failure")
        )

        service = RestaurantService(mock_restaurant_repo, archive_repo)

        # Act & Assert - Should raise exception
        with pytest.raises(Exception, match="Simulated delete failure"):
            await service.delete_restaurant(
                restaurant_id=restaurant_id,
                deleted_by="user123",
                note="Should rollback",
            )

        # Assert - Restaurant still exists (delete failed as expected)
        result = await test_session.exec(
            select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
        )
        restaurant_after = result.first()
        assert restaurant_after is not None

        # Assert - No archive created (rollback worked)
        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == restaurant_id)
        )
        assert result.first() is None


class TestRestaurantServiceDeleteValidation:
    """Test suite for delete validation logic."""

    @pytest.mark.asyncio
    async def test_delete_nonexistent_restaurant(self, test_session: AsyncSession):
        """Test deleting non-existent restaurant raises exception.

        Given: A restaurant ID that doesn't exist
        When: Calling delete_restaurant
        Then: Raises RestaurantNotFoundException
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"

        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)

        # Act & Assert
        with pytest.raises(RestaurantNotFoundException):
            await service.delete_restaurant(
                restaurant_id=nonexistent_id,
                deleted_by="user123",
                note="Should fail",
            )

    @pytest.mark.asyncio
    async def test_delete_without_note(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test deletion without note is allowed.

        Given: A restaurant exists
        When: Calling delete_restaurant without note
        Then: Delete succeeds and archive has no note
        """
        # Arrange
        restaurant = await create_test_restaurant(name="No Note Test")
        restaurant_id = restaurant.id

        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)

        # Act
        await service.delete_restaurant(
            restaurant_id=restaurant_id,
            deleted_by="user123",
            note=None,  # Explicitly no note
        )

        # Assert - Archive created without note
        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == restaurant_id)
        )
        archive = result.first()
        assert archive is not None
        assert archive.note is None

    @pytest.mark.asyncio
    async def test_delete_preserves_all_restaurant_data(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test that archive contains complete restaurant data.

        Given: A restaurant with complete data exists
        When: Calling delete_restaurant
        Then: Archive contains all restaurant fields
        """
        # Arrange
        restaurant = await create_test_restaurant(
            name="Complete Data Test",
            description="Full description here",
            email="test@restaurant.com",
            phone="+57 300 123 4567",
            price_level=3,
        )
        restaurant_id = restaurant.id

        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)

        # Act
        await service.delete_restaurant(
            restaurant_id=restaurant_id,
            deleted_by="admin123",
            note="Archiving complete data",
        )

        # Assert - All data preserved in archive
        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == restaurant_id)
        )
        archive = result.first()
        assert archive is not None
        assert archive.data["name"] == "Complete Data Test"
        assert archive.data["description"] == "Full description here"
        assert archive.data["email"] == "test@restaurant.com"
        assert archive.data["phone"] == "+57 300 123 4567"
        assert archive.data["price_level"] == 3
        assert archive.deleted_by == "admin123"
        assert archive.note == "Archiving complete data"
