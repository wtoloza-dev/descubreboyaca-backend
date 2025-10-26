"""Integration tests for UserRepository update operations.

These tests verify user update and deactivation through the repository layer with database.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.auth.domain import UserData
from app.domains.auth.domain.enums import AuthProvider, UserRole
from app.domains.auth.repositories.user import UserRepositorySQLite


class TestUserRepositoryUpdate:
    """Integration tests for UserRepository update operation."""

    @pytest.mark.asyncio
    async def test_update_user_with_new_data(
        self,
        test_session: AsyncSession,
        user_repository: UserRepositorySQLite,
        create_test_user,
    ):
        """Test updating user with new data.

        Given: User exists in database
        When: Calling repository.update() with new data
        Then: Updates user and returns updated entity
        """
        # Arrange
        user = await create_test_user(
            email="original@example.com",
            full_name="Original Name",
        )

        update_data = UserData(
            email="original@example.com",
            full_name="Updated Name",
            hashed_password=user.hashed_password,
        )

        # Act
        updated_user = await user_repository.update(user.id, update_data)

        # Assert
        assert updated_user is not None
        assert updated_user.id == user.id
        assert updated_user.full_name == "Updated Name"
        assert updated_user.updated_at is not None

    @pytest.mark.asyncio
    async def test_update_nonexistent_user_returns_none(
        self,
        test_session: AsyncSession,
        user_repository: UserRepositorySQLite,
    ):
        """Test updating non-existent user returns None.

        Given: User ID does not exist
        When: Calling repository.update()
        Then: Returns None
        """
        # Arrange
        from app.shared.domain.factories import generate_ulid

        nonexistent_id = generate_ulid()
        update_data = UserData(
            email="doesntmatter@example.com",
            full_name="Doesnt Matter",
            hashed_password="password",
        )

        # Act
        result = await user_repository.update(nonexistent_id, update_data)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_update_user_role(
        self,
        test_session: AsyncSession,
        user_repository: UserRepositorySQLite,
        create_test_user,
    ):
        """Test updating user role.

        Given: User with USER role
        When: Calling repository.update() with ADMIN role
        Then: Updates role to ADMIN
        """
        # Arrange
        user = await create_test_user(
            email="rolechange@example.com",
            role=UserRole.USER,
        )

        update_data = UserData(
            email="rolechange@example.com",
            full_name=user.full_name,
            hashed_password=user.hashed_password,
            role=UserRole.ADMIN,
        )

        # Act
        updated_user = await user_repository.update(user.id, update_data)

        # Assert
        assert updated_user is not None
        assert updated_user.role == UserRole.ADMIN

    @pytest.mark.asyncio
    async def test_update_user_oauth_fields(
        self,
        test_session: AsyncSession,
        user_repository: UserRepositorySQLite,
        create_test_user,
    ):
        """Test updating user with OAuth provider information.

        Given: User with EMAIL auth provider
        When: Calling repository.update() with Google OAuth data
        Then: Updates auth_provider and google_id
        """
        # Arrange
        user = await create_test_user(
            email="upgrade@example.com",
            auth_provider=AuthProvider.EMAIL,
        )

        update_data = UserData(
            email="upgrade@example.com",
            full_name=user.full_name,
            hashed_password=user.hashed_password,
            auth_provider=AuthProvider.GOOGLE,
            google_id="google_oauth_new_123",
            profile_picture_url="https://example.com/new_pic.jpg",
        )

        # Act
        updated_user = await user_repository.update(user.id, update_data)

        # Assert
        assert updated_user is not None
        assert updated_user.auth_provider == AuthProvider.GOOGLE
        assert updated_user.google_id == "google_oauth_new_123"
        assert updated_user.profile_picture_url == "https://example.com/new_pic.jpg"

    @pytest.mark.asyncio
    async def test_update_sets_updated_at_timestamp(
        self,
        test_session: AsyncSession,
        user_repository: UserRepositorySQLite,
        create_test_user,
    ):
        """Test update sets updated_at timestamp.

        Given: User exists
        When: Calling repository.update()
        Then: Sets updated_at to current time
        """
        # Arrange
        user = await create_test_user(email="timestamp@example.com")
        original_created_at = user.created_at

        update_data = UserData(
            email="timestamp@example.com",
            full_name="Updated Name",
            hashed_password=user.hashed_password,
        )

        # Act
        updated_user = await user_repository.update(user.id, update_data)

        # Assert
        assert updated_user is not None
        assert updated_user.updated_at is not None
        assert updated_user.created_at == original_created_at  # Shouldn't change

    @pytest.mark.asyncio
    async def test_update_without_commit(
        self,
        test_session: AsyncSession,
        user_repository: UserRepositorySQLite,
        create_test_user,
    ):
        """Test updating user without auto-commit.

        Given: commit=False parameter
        When: Calling repository.update()
        Then: Changes are not immediately committed
        """
        # Arrange
        user = await create_test_user(
            email="nocommit@example.com",
            full_name="Original",
        )

        update_data = UserData(
            email="nocommit@example.com",
            full_name="Updated",
            hashed_password=user.hashed_password,
        )

        # Act
        updated_user = await user_repository.update(user.id, update_data, commit=False)

        # Assert - commit manually
        await user_repository.commit()
        retrieved_user = await user_repository.get_by_id(user.id)
        assert retrieved_user is not None
        assert retrieved_user.full_name == "Updated"


class TestUserRepositoryDeactivate:
    """Integration tests for UserRepository deactivate operation."""

    @pytest.mark.asyncio
    async def test_deactivate_existing_user(
        self,
        test_session: AsyncSession,
        user_repository: UserRepositorySQLite,
        create_test_user,
    ):
        """Test deactivating existing user.

        Given: Active user exists
        When: Calling repository.deactivate()
        Then: Sets is_active to False and returns True
        """
        # Arrange
        user = await create_test_user(
            email="active@example.com",
            is_active=True,
        )

        # Act
        result = await user_repository.deactivate(user.id)

        # Assert
        assert result is True
        deactivated_user = await user_repository.get_by_id(user.id)
        assert deactivated_user is not None
        assert deactivated_user.is_active is False

    @pytest.mark.asyncio
    async def test_deactivate_nonexistent_user(
        self,
        test_session: AsyncSession,
        user_repository: UserRepositorySQLite,
    ):
        """Test deactivating non-existent user returns False.

        Given: User ID does not exist
        When: Calling repository.deactivate()
        Then: Returns False
        """
        # Arrange
        from app.shared.domain.factories import generate_ulid

        nonexistent_id = generate_ulid()

        # Act
        result = await user_repository.deactivate(nonexistent_id)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_deactivate_sets_updated_at(
        self,
        test_session: AsyncSession,
        user_repository: UserRepositorySQLite,
        create_test_user,
    ):
        """Test deactivate updates the updated_at timestamp.

        Given: Active user exists
        When: Calling repository.deactivate()
        Then: Sets updated_at to current time
        """
        # Arrange
        user = await create_test_user(email="timestamp@example.com")

        # Act
        result = await user_repository.deactivate(user.id)

        # Assert
        assert result is True
        deactivated_user = await user_repository.get_by_id(user.id)
        assert deactivated_user is not None
        assert deactivated_user.updated_at is not None

    @pytest.mark.asyncio
    async def test_deactivate_already_inactive_user(
        self,
        test_session: AsyncSession,
        user_repository: UserRepositorySQLite,
        create_test_user,
    ):
        """Test deactivating already inactive user.

        Given: User is already inactive
        When: Calling repository.deactivate()
        Then: Returns True (idempotent)
        """
        # Arrange
        user = await create_test_user(
            email="alreadyinactive@example.com",
            is_active=False,
        )

        # Act
        result = await user_repository.deactivate(user.id)

        # Assert
        assert result is True
        user_check = await user_repository.get_by_id(user.id)
        assert user_check is not None
        assert user_check.is_active is False
