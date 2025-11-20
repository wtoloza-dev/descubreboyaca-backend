"""Delete user use case."""

from app.domains.audit.domain import Archive, ArchiveData
from app.domains.audit.domain.interfaces import ArchiveRepositoryInterface
from app.domains.users.domain.exceptions import UserNotFoundException
from app.domains.users.domain.interfaces import UserRepositoryInterface


class DeleteUserUseCase:
    """Use case for deleting a user with archiving.

    This use case:
    1. Archives the user data for audit purposes
    2. Deletes the user from the active table

    Both operations are performed atomically to ensure data consistency.

    Attributes:
        user_repository: Repository for user persistence
        archive_repository: Repository for archive persistence (soft delete)
    """

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        archive_repository: ArchiveRepositoryInterface,
    ) -> None:
        """Initialize use case.

        Args:
            user_repository: User repository implementation
            archive_repository: Archive repository implementation
        """
        self.user_repository = user_repository
        self.archive_repository = archive_repository

    async def execute(
        self, user_id: str, deleted_by: str, note: str | None = None
    ) -> None:
        """Execute the delete user use case.

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
