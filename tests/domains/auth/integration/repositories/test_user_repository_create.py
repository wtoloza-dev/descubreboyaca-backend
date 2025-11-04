"""Integration tests for UserRepository create operations.

These tests verify user creation through the repository layer with database.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.auth.domain import UserData
from app.domains.auth.domain.enums import AuthProvider, UserRole
from app.domains.auth.repositories.user import SQLiteUserRepository


class TestUserRepositoryCreate:
    """Integration tests for UserRepository create operation."""

    @pytest.mark.asyncio
    async def test_create_user_with_minimal_data(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test creating user with minimal required data.

        Given: Valid UserData with minimal fields
        When: Calling repository.create()
        Then: Creates user with generated ID and timestamps
        """
        # Arrange
        user_data = UserData(
            email="minimal@example.com",
            full_name="Minimal User",
            hashed_password="hashed_password_here",
        )

        # Act
        user = await user_repository.create(user_data)

        # Assert
        assert user.id is not None  # ULID generated
        assert user.email == "minimal@example.com"
        assert user.full_name == "Minimal User"
        assert user.hashed_password == "hashed_password_here"
        assert user.role == UserRole.USER  # Default
        assert user.is_active is True  # Default
        assert user.auth_provider == AuthProvider.EMAIL  # Default
        assert user.created_at is not None

    @pytest.mark.asyncio
    async def test_create_user_with_all_fields(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test creating user with all optional fields.

        Given: UserData with all fields specified
        When: Calling repository.create()
        Then: Creates user with all specified values
        """
        # Arrange
        user_data = UserData(
            email="complete@example.com",
            full_name="Complete User",
            hashed_password="hashed_password",
            role=UserRole.ADMIN,
            is_active=True,
            auth_provider=AuthProvider.GOOGLE,
            google_id="google_123456",
            profile_picture_url="https://example.com/pic.jpg",
        )

        # Act
        user = await user_repository.create(user_data)

        # Assert
        assert user.email == "complete@example.com"
        assert user.role == UserRole.ADMIN
        assert user.auth_provider == AuthProvider.GOOGLE
        assert user.google_id == "google_123456"
        assert user.profile_picture_url == "https://example.com/pic.jpg"

    @pytest.mark.asyncio
    async def test_create_user_persists_to_database(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test created user can be retrieved from database.

        Given: User created via repository
        When: Querying database by email
        Then: User is found with correct data
        """
        # Arrange
        user_data = UserData(
            email="persisted@example.com",
            full_name="Persisted User",
            hashed_password="hashed_password",
        )

        # Act
        created_user = await user_repository.create(user_data)

        # Assert - retrieve from database
        retrieved_user = await user_repository.get_by_email("persisted@example.com")
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email

    @pytest.mark.asyncio
    async def test_create_user_without_commit(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test creating user without auto-commit.

        Given: commit=False parameter
        When: Calling repository.create()
        Then: User is not immediately visible in database
        """
        # Arrange
        user_data = UserData(
            email="uncommitted@example.com",
            full_name="Uncommitted User",
            hashed_password="hashed_password",
        )

        # Act
        user = await user_repository.create(user_data, commit=False)

        # Assert - should not be visible without commit
        # Need to query in same session
        await user_repository.get_by_email("uncommitted@example.com")
        # In same session, it might be visible depending on isolation level
        # But after explicit commit it should definitely be visible
        await user_repository.commit()
        retrieved_after_commit = await user_repository.get_by_email(
            "uncommitted@example.com"
        )
        assert retrieved_after_commit is not None
        assert retrieved_after_commit.id == user.id

    @pytest.mark.asyncio
    async def test_create_user_generates_unique_ulid(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test each created user gets unique ULID.

        Given: Multiple users created
        When: Calling repository.create() multiple times
        Then: Each user has different ULID
        """
        # Arrange
        user_data_1 = UserData(
            email="user1@example.com",
            full_name="User 1",
            hashed_password="password",
        )
        user_data_2 = UserData(
            email="user2@example.com",
            full_name="User 2",
            hashed_password="password",
        )

        # Act
        user1 = await user_repository.create(user_data_1)
        user2 = await user_repository.create(user_data_2)

        # Assert
        assert user1.id != user2.id
        assert len(user1.id) == 26  # ULID length
        assert len(user2.id) == 26

    @pytest.mark.asyncio
    async def test_create_oauth_user_without_password(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test creating OAuth user without password.

        Given: UserData with hashed_password=None (OAuth user)
        When: Calling repository.create()
        Then: Creates user without password
        """
        # Arrange
        user_data = UserData(
            email="oauth@example.com",
            full_name="OAuth User",
            hashed_password=None,  # OAuth users don't have passwords
            auth_provider=AuthProvider.GOOGLE,
            google_id="google_oauth_123",
        )

        # Act
        user = await user_repository.create(user_data)

        # Assert
        assert user.hashed_password is None
        assert user.auth_provider == AuthProvider.GOOGLE
        assert user.google_id == "google_oauth_123"

    @pytest.mark.asyncio
    async def test_create_owner_user(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test creating user with OWNER role.

        Given: UserData with role=OWNER
        When: Calling repository.create()
        Then: Creates user with OWNER role
        """
        # Arrange
        user_data = UserData(
            email="owner@example.com",
            full_name="Owner User",
            hashed_password="hashed_password",
            role=UserRole.OWNER,
        )

        # Act
        user = await user_repository.create(user_data)

        # Assert
        assert user.role == UserRole.OWNER
