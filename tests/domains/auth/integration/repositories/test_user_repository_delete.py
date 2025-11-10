"""Integration tests for UserRepository delete operations.

These tests verify user deletion (hard delete) through the repository layer with database.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.auth.infrastructure.persistence.repositories.user import (
    SQLiteUserRepository,
)


class TestUserRepositoryDelete:
    """Integration tests for UserRepository delete operation."""

    @pytest.mark.asyncio
    async def test_delete_existing_user(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test deleting existing user removes it from database.

        Given: User exists in database
        When: Calling repository.delete()
        Then: Removes user and returns True
        """
        # Arrange
        user = await create_test_user(email="todelete@example.com")

        # Act
        result = await user_repository.delete(user.id)

        # Assert
        assert result is True
        deleted_user = await user_repository.get_by_id(user.id)
        assert deleted_user is None  # User should not exist

    @pytest.mark.asyncio
    async def test_delete_nonexistent_user(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test deleting non-existent user returns False.

        Given: User ID does not exist
        When: Calling repository.delete()
        Then: Returns False
        """
        # Arrange
        from app.shared.domain.factories import generate_ulid

        nonexistent_id = generate_ulid()

        # Act
        result = await user_repository.delete(nonexistent_id)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_delete_removes_user_permanently(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test delete is permanent (hard delete).

        Given: User exists
        When: Calling repository.delete()
        Then: User cannot be retrieved by any method
        """
        # Arrange
        user = await create_test_user(
            email="permanent@example.com",
            google_id="google_123",
        )
        user_id = user.id
        email = user.email
        google_id = user.google_id

        # Act
        result = await user_repository.delete(user_id)

        # Assert
        assert result is True
        # Try all get methods
        assert await user_repository.get_by_id(user_id) is None
        assert await user_repository.get_by_email(email) is None
        assert await user_repository.get_by_google_id(google_id) is None

    @pytest.mark.asyncio
    async def test_delete_without_commit(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test deleting user without auto-commit.

        Given: commit=False parameter
        When: Calling repository.delete()
        Then: Changes are not immediately committed
        """
        # Arrange
        user = await create_test_user(email="nocommit@example.com")

        # Act
        result = await user_repository.delete(user.id, commit=False)

        # Assert
        assert result is True
        # Commit manually
        await user_repository.commit()
        deleted_user = await user_repository.get_by_id(user.id)
        assert deleted_user is None

    @pytest.mark.asyncio
    async def test_delete_twice_returns_false_second_time(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test deleting same user twice returns False second time.

        Given: User exists
        When: Calling repository.delete() twice
        Then: First call returns True, second returns False
        """
        # Arrange
        user = await create_test_user(email="deletetwice@example.com")

        # Act
        first_result = await user_repository.delete(user.id)
        second_result = await user_repository.delete(user.id)

        # Assert
        assert first_result is True
        assert second_result is False


class TestUserRepositoryTransactions:
    """Integration tests for UserRepository transaction operations."""

    @pytest.mark.asyncio
    async def test_commit_persists_changes(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test commit persists pending changes.

        Given: User created without auto-commit
        When: Calling repository.commit()
        Then: Changes are persisted to database
        """
        # Arrange
        from app.domains.users.domain import UserData

        user_data = UserData(
            email="committest@example.com",
            full_name="Commit Test",
            hashed_password="password",
        )

        # Act
        user = await user_repository.create(user_data, commit=False)
        await user_repository.commit()

        # Assert
        retrieved_user = await user_repository.get_by_id(user.id)
        assert retrieved_user is not None
        assert retrieved_user.email == "committest@example.com"

    @pytest.mark.asyncio
    async def test_rollback_reverts_changes(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test rollback reverts pending changes.

        Given: User updated without auto-commit
        When: Calling repository.rollback()
        Then: Changes are reverted
        """
        # Arrange
        from app.domains.users.domain import UserData

        user = await create_test_user(
            email="rollback@example.com",
            full_name="Original Name",
        )

        update_data = UserData(
            email="rollback@example.com",
            full_name="Updated Name",
            hashed_password=user.hashed_password,
        )

        # Act
        await user_repository.update(user.id, update_data, commit=False)
        await user_repository.rollback()

        # Assert
        retrieved_user = await user_repository.get_by_id(user.id)
        assert retrieved_user is not None
        assert retrieved_user.full_name == "Original Name"  # Reverted
