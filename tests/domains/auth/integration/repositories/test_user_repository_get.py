"""Integration tests for UserRepository get operations.

These tests verify user retrieval through the repository layer with database.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.auth.infrastructure.persistence.repositories.user import (
    SQLiteUserRepository,
)
from app.domains.users.domain.enums import AuthProvider


class TestUserRepositoryGet:
    """Integration tests for UserRepository get operations."""

    @pytest.mark.asyncio
    async def test_get_by_id_existing_user(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test getting existing user by ID returns user.

        Given: User exists in database
        When: Calling repository.get_by_id()
        Then: Returns User entity
        """
        # Arrange
        user = await create_test_user(email="existing@example.com")

        # Act
        retrieved_user = await user_repository.get_by_id(user.id)

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.email == user.email

    @pytest.mark.asyncio
    async def test_get_by_id_nonexistent_user(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test getting non-existent user by ID returns None.

        Given: User ID does not exist
        When: Calling repository.get_by_id()
        Then: Returns None
        """
        # Arrange
        from app.shared.domain.factories import generate_ulid

        nonexistent_id = generate_ulid()

        # Act
        user = await user_repository.get_by_id(nonexistent_id)

        # Assert
        assert user is None

    @pytest.mark.asyncio
    async def test_get_by_email_existing_user(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test getting existing user by email returns user.

        Given: User exists in database
        When: Calling repository.get_by_email()
        Then: Returns User entity
        """
        # Arrange
        user = await create_test_user(email="email@example.com", full_name="Email User")

        # Act
        retrieved_user = await user_repository.get_by_email("email@example.com")

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.email == "email@example.com"
        assert retrieved_user.full_name == "Email User"

    @pytest.mark.asyncio
    async def test_get_by_email_nonexistent_user(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test getting non-existent user by email returns None.

        Given: Email does not exist
        When: Calling repository.get_by_email()
        Then: Returns None
        """
        # Arrange & Act
        user = await user_repository.get_by_email("nonexistent@example.com")

        # Assert
        assert user is None

    @pytest.mark.asyncio
    async def test_get_by_email_case_sensitive(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test email lookup is case-sensitive.

        Given: User with lowercase email
        When: Calling repository.get_by_email() with different case
        Then: Returns None (case-sensitive)
        """
        # Arrange
        await create_test_user(email="lowercase@example.com")

        # Act
        retrieved_user = await user_repository.get_by_email("LOWERCASE@EXAMPLE.COM")

        # Assert
        assert retrieved_user is None  # Case-sensitive

    @pytest.mark.asyncio
    async def test_get_by_google_id_existing_user(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test getting existing user by Google ID returns user.

        Given: User with Google OAuth ID exists
        When: Calling repository.get_by_google_id()
        Then: Returns User entity
        """
        # Arrange
        user = await create_test_user(
            email="google@example.com",
            auth_provider=AuthProvider.GOOGLE,
            google_id="google_oauth_123456",
        )

        # Act
        retrieved_user = await user_repository.get_by_google_id("google_oauth_123456")

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.google_id == "google_oauth_123456"

    @pytest.mark.asyncio
    async def test_get_by_google_id_nonexistent_user(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
    ):
        """Test getting non-existent user by Google ID returns None.

        Given: Google ID does not exist
        When: Calling repository.get_by_google_id()
        Then: Returns None
        """
        # Arrange & Act
        user = await user_repository.get_by_google_id("nonexistent_google_id")

        # Assert
        assert user is None

    @pytest.mark.asyncio
    async def test_get_by_id_returns_all_user_fields(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test get_by_id returns user with all fields populated.

        Given: User with all fields set
        When: Calling repository.get_by_id()
        Then: Returns user with all fields
        """
        # Arrange
        user = await create_test_user(
            email="complete@example.com",
            full_name="Complete User",
            hashed_password="hashed_password",
            auth_provider=AuthProvider.GOOGLE,
            google_id="google_123",
            profile_picture_url="https://example.com/pic.jpg",
        )

        # Act
        retrieved_user = await user_repository.get_by_id(user.id)

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.email == "complete@example.com"
        assert retrieved_user.full_name == "Complete User"
        assert retrieved_user.hashed_password == "hashed_password"
        assert retrieved_user.auth_provider == AuthProvider.GOOGLE
        assert retrieved_user.google_id == "google_123"
        assert retrieved_user.profile_picture_url == "https://example.com/pic.jpg"
        assert retrieved_user.created_at is not None

    @pytest.mark.asyncio
    async def test_get_inactive_user_by_email(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test getting inactive user by email returns user.

        Given: User exists but is_active=False
        When: Calling repository.get_by_email()
        Then: Returns User entity (repository doesn't filter by active status)
        """
        # Arrange
        await create_test_user(
            email="inactive@example.com",
            is_active=False,
        )

        # Act
        retrieved_user = await user_repository.get_by_email("inactive@example.com")

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.is_active is False

    @pytest.mark.asyncio
    async def test_get_by_email_with_special_characters(
        self,
        test_session: AsyncSession,
        user_repository: SQLiteUserRepository,
        create_test_user,
    ):
        """Test getting user with special characters in email.

        Given: User with special characters in email
        When: Calling repository.get_by_email()
        Then: Returns User entity
        """
        # Arrange
        await create_test_user(
            email="user+test@example.com",  # Plus sign
            full_name="Special User",
        )

        # Act
        retrieved_user = await user_repository.get_by_email("user+test@example.com")

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.email == "user+test@example.com"
