"""User service implementation for admin operations.

This module provides the user management service for administrative operations.
"""

from app.domains.audit.domain import Archive, ArchiveData
from app.domains.audit.domain.interfaces import ArchiveRepositoryInterface
from app.domains.auth.domain import User, UserData
from app.domains.auth.domain.enums import AuthProvider, UserRole
from app.domains.auth.domain.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.domains.auth.domain.interfaces import (
    PasswordHasher,
    UserRepositoryInterface,
)


class UserService:
    """User management service for admin operations.

    This service provides CRUD operations for users,
    restricted to administrative use only.

    Attributes:
        user_repository: Repository for user persistence
        archive_repository: Repository for archive persistence (soft delete)
        password_hasher: Hasher for password operations
    """

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        archive_repository: ArchiveRepositoryInterface,
        password_hasher: PasswordHasher,
    ) -> None:
        """Initialize user service.

        Args:
            user_repository: User repository implementation
            archive_repository: Archive repository implementation
            password_hasher: Password hasher implementation
        """
        self.user_repository = user_repository
        self.archive_repository = archive_repository
        self.password_hasher = password_hasher

    async def create(
        self,
        email: str,
        password: str,
        full_name: str,
        role: UserRole,
        is_active: bool,
        created_by: str,
    ) -> User:
        """Create a new user (admin operation).

        Args:
            email: User's email address
            password: Plain text password
            full_name: User's full name
            role: User's role in the system
            is_active: Whether the account is active
            created_by: Admin user ID who created this user

        Returns:
            Created User entity

        Raises:
            UserAlreadyExistsException: If email is already registered
        """
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise UserAlreadyExistsException(email)

        # Hash password
        hashed_password = self.password_hasher.hash_password(password)

        # Create user data
        user_data = UserData(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password.value,
            role=role,
            is_active=is_active,
            auth_provider=AuthProvider.EMAIL,
        )

        # Persist user
        user = await self.user_repository.create(user_data, created_by=created_by)

        return user

    async def find_all(
        self, offset: int = 0, limit: int = 20
    ) -> tuple[list[User], int]:
        """Find all users with pagination.

        Args:
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of users, total count)
        """
        # Get users from repository
        users = await self.user_repository.find(
            filters=None, offset=offset, limit=limit
        )

        # Get total count
        total = await self.user_repository.count(filters=None)

        return users, total

    async def delete(
        self, user_id: str, deleted_by: str, note: str | None = None
    ) -> None:
        """Delete a user with archiving (soft delete + archive).

        This method:
        1. Archives the user data for audit purposes
        2. Deletes the user from the active table

        Args:
            user_id: ULID of the user to delete
            deleted_by: Admin user ID who performed the deletion
            note: Optional note explaining the deletion

        Raises:
            UserNotFoundException: If user doesn't exist
        """
        # Get user before deletion
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)

        # Create archive entry
        archive_data = ArchiveData(
            table_name="users",
            record_id=user.id,
            data=user.model_dump(mode="json"),
            note=note,
        )
        archive = Archive(**archive_data.model_dump(), deleted_by=deleted_by)

        # Save to archive and delete user (atomic operation)
        try:
            await self.archive_repository.create(archive, commit=False)
            await self.user_repository.delete(
                user_id, deleted_by=deleted_by, commit=False
            )
            await self.user_repository.commit()
        except Exception:
            await self.user_repository.rollback()
            raise
